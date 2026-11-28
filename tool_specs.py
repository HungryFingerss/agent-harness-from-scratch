TOOL_SPECS = [
        {
          "type": "function",
          "function": {
            "name": "find_customer",
            "description": "Identify the customer by their email address. Call this first, before any tool that uses the customer's own data (their orders, invoice details, or support rep). If found, returns the customer's first and last name. If not found, returns a message asking the customer to re-check their email.",
            "parameters": {
              "type": "object",
              "properties": {
                "email": {
                  "type": "string",
                  "description": "customer's email address. example: customer@gmail.com"
                }
              },
              "required": ["email"]
            }
          }
        },

        {
          "type": "function",
          "function": {
            "name": "invoice_lines",
            "description": "customer must be identified to use this tool. use this tool to get a particular invoice/order details. if the tool call is succeed, it will return the track name, unit price and quantity. if fails, it returns the appropriate action to do next",
            "parameters": {
              "type": "object",
              "properties": {
                "invoice_id": {
                  "type": "integer",
                  "description": "the particular invoice_id that the customer asked details about"
                }
              },
              "required": ["invoice_id"]
            }
          }
        },

        {
          "type": "function",
          "function": {
            "name": "search_tracks",
            "description": "no need for verification or ask for customer email to use this tool. use this when a customer asked about tracks from a partiular artis. if the tool call is succeed, it will return the track name, unit price and album title. At most 10 results when success. if fails, it returns the appropriate action to do next",
            "parameters": {
              "type": "object",
              "properties": {
                "artist": {
                  "type": "string",
                  "description": "name of the artist"
                }
              },
              "required": ["artist"]
            }
          }
        },

        {
          "type": "function",
          "function": {
            "name": "support_rep",
            "description": "customer must be identified to use this tool. use this when customer asked details about his/her support representative details. if the tool call is succeed, it will return the first name, last name and support representative's email. if fails, it returns the appropriate action to do next",
            "parameters": {"type": "object", "properties": {}}
            }
        },

        {
          "type": "function",
          "function": {
            "name": "list_invoices",
            "description": "customer must be identified to use this tool. use this when customer asked details about his/her list of orders or all the orders/invoices. if the tool call is succeed, it will return the invoice id, incoice date and invoice total for all the invoices/orders under this customer. if fails, it returns the appropriate action to do next",
            "parameters": {"type": "object", "properties": {}}
            }
        },
        

]