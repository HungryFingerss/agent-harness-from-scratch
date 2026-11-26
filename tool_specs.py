TOOL_SPECS = [
        {
          "type": "function",
          "function": {
            "name": "find_customer",
            "description": "Get current customer details",
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
]