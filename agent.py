import tools
import json
import llm
import tool_specs as ToolSpecs

def run_tool(name, args, state):
    try: 
        if name == "find_customer":
            tool_res = tools.find_customer(args['email'])
            state["customer_id"] = tool_res["customer_id"]
            tool_res_to_llm = json.dumps({"first_name": tool_res["first_name"], "last_name": tool_res["last_name"]})
    
        elif name == 'list_invoices':
            if state['customer_id'] is None:
                tool_res_to_llm = "Identify the customer first: ask for their email."
                return tool_res_to_llm
            tool_res = tools.list_invoices(state['customer_id'])
            if tool_res == []:
                tool_res_to_llm = "this customer dont have any invoices, i.e: this customer havent ordered anything yet"
                return tool_res_to_llm
            else:
                tool_res_to_llm = []
                for invoice in tool_res:
                    tool_res_to_llm.append({"invoice_id": invoice["invoice_id"], "invoice_date": invoice["invoice_date"], "invoice_total": invoice["invoice_total"]})
                return json.dumps(tool_res_to_llm)
    
        elif name == 'invoice_lines':
            if state['customer_id'] is None:
                tool_res_to_llm = "Identify the customer first: ask for their email."
                return tool_res_to_llm
            if 'invoice_id' not in args:
                return "Please add or ask the customer for invoice id"
            tool_res = tools.invoice_lines(state['customer_id'], args['invoice_id'])
            tool_res_to_llm = json.dumps(tool_res)
    
        elif name == 'support_rep':
            if state['customer_id'] is None:
                tool_res_to_llm = "Identify the customer first: ask for their email."
                return tool_res_to_llm
            tool_res = tools.support_rep(state['customer_id'])
            tool_res_to_llm = json.dumps(tool_res)
    
        elif name == 'search_tracks':
            if 'artist' not in args:
                return "Please add or ask the customer for artist name"
            tool_res = tools.search_tracks(args['artist'])
            tool_res_to_llm = json.dumps(tool_res)

        else:
            return f"Unknown tool: {name}"

    
    except tools.ToolError as e:
        tool_res_to_llm = str(e)

    except Exception as e:
        tool_res_to_llm = "Tool failed due to an internal error. Apologise and ask the customer to try again later."

    return tool_res_to_llm


def respond(user_text, history, state):
    history.append({"role": "user", "content": user_text})

    for repeat in range(8):
        reply = llm.chat(history, ToolSpecs.TOOL_SPECS)
        history.append(reply)

        if not reply.get("tool_calls"):
            return reply["content"]

        for call in reply['tool_calls']:
            tool_id = call['id']
            tool_name = call['function']['name']

            try:
                tool_args = json.loads(call['function']['arguments'])
            except json.JSONDecodeError as e:
                tool_result = (f"Invalid arguments for tool '{tool_name}': {e}. Please provide valid JSON arguments and try again.")
                history.append({"role": "tool", 'tool_call_id': tool_id, "content": tool_result})
                continue


            print("TOOL:", tool_name, tool_args)
            tool_result = run_tool(tool_name, tool_args, state)
            history.append({"role": "tool", 'tool_call_id': tool_id, "content": tool_result})

    return "Sorry, I couldn't complete that."







state = {'customer_id': None}
history = []

print(respond("Hi, my email is manoj.pareek@rediff.com", history, state))
print(respond("What's in my latest order?", history, state))

print("full round: ", history)