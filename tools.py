import sqlite3

class ToolError(Exception):
    pass

connection = sqlite3.connect('Chinook_Sqlite.sqlite')
cur = connection.cursor()


def find_customer(email):
    email = email.strip().lower()
    found = cur.execute(" SELECT CustomerId, FirstName, LastName, Email FROM Customer WHERE lower(Email) = ?", (email,)).fetchone()
    if found is None:
        raise ToolError(f'the customer email: {email} is not found, ask the customer to check the mail he entered and try again')
    return {"customer_id": found[0], "first_name": found[1], "last_name": found[2], "email": found[3]}
    # return {"customer_id": found[0], "first_name": found[1], "last_name": found[2]}

def support_rep(customer_id):
    found = cur.execute(""" SELECT e.FirstName, e.LastName, e.Email
    FROM Customer c
    JOIN Employee e ON e.EmployeeId = c.SupportRepId
    WHERE c.CustomerId = ?""", (customer_id,)).fetchone()

    if found is None:
        raise ToolError(f'the customer id: {customer_id} is invalid, code problem')
    return {"first_name": found[0], "last_name": found[1], "support_rep_email": found[2]}

def list_invoices(customer_id):
    found = cur.execute(""" SELECT InvoiceId, InvoiceDate, Total
    FROM Invoice
    WHERE CustomerId = ?
    ORDER BY InvoiceDate DESC""", (customer_id,)).fetchall()

    invoices = [] 
    for i in found:
        invoices.append({"invoice_id": i[0], "invoice_date": i[1], "invoice_total": i[2]})
    return invoices         # tool description when empty arry : "this customer dont have any invoices, that means, this customer dont have any orders yet" # for ai model to better understand than simply passing an empty array

def invoice_lines(customer_id, invoice_id):
    found = cur.execute("""SELECT t.Name, il.UnitPrice, il.Quantity
    FROM InvoiceLine il
    JOIN Invoice i ON i.InvoiceId = il.InvoiceId
    JOIN Track t   ON t.TrackId   = il.TrackId
    WHERE i.CustomerId = ? AND il.InvoiceId = ?""", (customer_id,invoice_id,)).fetchall()
    if not found:
        raise ToolError('Not found or not belong to this customer, please ask customer to recheck his invoice id and try again')
    res = [] 
    for i in found:
        res.append({"track_name": i[0], "unit_price": i[1], "quantity": i[2]})
    return res

def search_tracks(artist):
    found = cur.execute(""" SELECT t.Name, al.Title, t.UnitPrice
    FROM Track t
    JOIN Album al  ON al.AlbumId  = t.AlbumId
    JOIN Artist ar ON ar.ArtistId = al.ArtistId
    WHERE ar.Name LIKE ?
    LIMIT 10""", ((f'%{artist}%'),)).fetchall()

    res = [] 
    for i in found:
        res.append({"track_name": i[0], "album_title": i[1], "unit_price": i[2]})
    return res

def check_new_email(customer_id, new_email):
    if "@" not in new_email:
        raise ToolError('the entered mail is invalid, please ask the customer to enter a valid mail address')
    new_email = new_email.strip().lower()
    curr_mail = cur.execute("""SELECT Email FROM Customer WHERE CustomerId = ?""", (customer_id,)).fetchone()
    if curr_mail is None:
        raise ToolError(f'the customer id: {customer_id} is invalid, code problem')
    if curr_mail[0].strip().lower() == new_email:
        raise ToolError('the current email address and the new email address are identical, please ask customer to change the new mail address')
    check_duplicate_mail = cur.execute("""SELECT CustomerId FROM Customer WHERE lower(Email) = ? AND CustomerId != ?""", (new_email, customer_id,)).fetchall()
    if check_duplicate_mail:
        raise ToolError('another customer already uses this email address, please ask the customer to change the new email address')
    return {"old_email": curr_mail[0],  "new_email": new_email}

def update_email(customer_id, new_email):
    verified = check_new_email(customer_id, new_email)
    cur.execute("""UPDATE Customer SET Email = ? WHERE CustomerId = ?""", (verified['new_email'],customer_id,))
    connection.commit()
    return verified
