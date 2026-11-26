import tools
import pytest
import shutil
import sqlite3

def use_fresh_copy():
    shutil.copy("Chinook_Sqlite.sqlite", "Copy_Chinook_Sqlite.sqlite")
    tools.connection = sqlite3.connect('Copy_Chinook_Sqlite.sqlite')
    tools.cur = tools.connection.cursor()

def test_correct_find_customer():
    use_fresh_copy()
    assert tools.find_customer("manoj.pareek@rediff.com") == {'customer_id': 58, 'first_name': 'Manoj', 'last_name': 'Pareek', 'email': 'manoj.pareek@rediff.com'}

def test_messy_correct_find_customer():
    use_fresh_copy()
    assert tools.find_customer("maNoj.parEEk@rediff.com") == {'customer_id': 58, 'first_name': 'Manoj', 'last_name': 'Pareek', 'email': 'manoj.pareek@rediff.com'}

def test_wrong_find_customer():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.find_customer("nobody@example.com")

def test_correct_support_rep():
    use_fresh_copy()
    assert tools.support_rep(58) == {'first_name': 'Jane', 'last_name': 'Peacock', 'support_rep_email': 'jane@chinookcorp.com'}

def test_wrong_support_rep():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.support_rep(9999)

def test_correct_list_invoices():
    use_fresh_copy()
    assert tools.list_invoices(58) == [{'invoice_id': 412, 'invoice_date': '2013-12-22 00:00:00', 'invoice_total': 1.99}, {'invoice_id': 360, 'invoice_date': '2013-05-03 00:00:00', 'invoice_total': 5.94}, {'invoice_id': 338, 'invoice_date': '2013-01-29 00:00:00', 'invoice_total': 3.96}, {'invoice_id': 315, 'invoice_date': '2012-10-27 00:00:00', 'invoice_total': 1.98}, {'invoice_id': 186, 'invoice_date': '2011-03-23 00:00:00', 'invoice_total': 8.91}, {'invoice_id': 131, 'invoice_date': '2010-07-23 00:00:00', 'invoice_total': 13.86}, {'invoice_id': 120, 'invoice_date': '2010-06-12 00:00:00', 'invoice_total': 1.98}]

def test_wrong_list_invoices():
    use_fresh_copy()
    assert tools.list_invoices(580000) == []

def test_correct_invoice_lines():
    use_fresh_copy()
    assert tools.invoice_lines(58, 412) == [{'track_name': 'Hot Girl', 'unit_price': 1.99, 'quantity': 1}]

def test_cannot_see_other_customers_invoice():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.invoice_lines(58, 1)

def test_correct_search_tracks():
    use_fresh_copy()
    assert tools.search_tracks('ac/dc') == [{'track_name': 'For Those About To Rock (We Salute You)', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Put The Finger On You', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': "Let's Get It Up", 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Inject The Venom', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Snowballed', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Evil Walks', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'C.O.D.', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Breaking The Rules', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Night Of The Long Knives', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}, {'track_name': 'Spellbound', 'album_title': 'For Those About To Rock We Salute You', 'unit_price': 0.99}]

def test_wrong_search_tracks():
    use_fresh_copy()
    assert tools.search_tracks('ac/dcjhkjhkjnl') == []

def test_correct_update_email():
    use_fresh_copy()
    assert tools.update_email(58, "manoj.new@gmail.com") == {"old_email": "manoj.pareek@rediff.com",  "new_email": "manoj.new@gmail.com"}
    assert tools.find_customer("manoj.new@gmail.com") == {'customer_id': 58, 'first_name': 'Manoj', 'last_name': 'Pareek', 'email': "manoj.new@gmail.com"}

def test_old_mail_stop_working():
    use_fresh_copy()
    tools.update_email(58, "manoj.new@gmail.com")
    with pytest.raises(tools.ToolError):
        tools.find_customer("manoj.pareek@rediff.com")

def test_same_mail_entered():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.check_new_email(58, "manoj.pareek@rediff.com")

def test_mail_taken():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.check_new_email(58, "luisg@embraer.com.br")

def test_invalid_mail_address():
    use_fresh_copy()
    with pytest.raises(tools.ToolError):
        tools.check_new_email(58, "bad-email")
