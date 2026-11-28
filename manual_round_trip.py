import llm
import tool_specs as toolSpecs
import json
import tools

history = []

user_message = "Hi, my name is Manoj"

history.append({
    "role": "user",
    "content": user_message
})

try:
    reply = llm.chat(history, toolSpecs.TOOL_SPECS)

    history.append(reply)

    print("Assistant:", reply)

except llm.llm.LLMError as e:
    history.pop()
    print(f"Problem: {e}")


user_message = "could you use my mail: manoj@gmail.com and give me all my details"

history.append({
    "role": "user",
    "content": user_message
})

try:
    reply = llm.chat(history, toolSpecs.TOOL_SPECS)
    
    history.append(reply)
    if 'tool_calls' in reply:
        print("Assistant:", reply)
        
        call = reply['tool_calls'][0]
        tool_id = call['id']
        tool_name = call['function']['name']
        tool_args = json.loads(call['function']['arguments'])["email"]

        try: 
            tool_res = json.dumps(tools.find_customer(tool_args))
            # tool_res = tools[tool_name](tool_args)
            print("tool res===", tool_res)
        except tools.ToolError as e:
            tool_res = str(e)
            print('problem==', e)

        history.append({'role': 'tool', 'tool_call_id': tool_id, 'content': tool_res})

except llm.LLMError as e:
    history.pop()
    print(f"Problem: {e}")

try:
    reply = llm.chat(history, toolSpecs.TOOL_SPECS)

    history.append(reply)

    print("Assistant:", reply['content'])

except llm.LLMError as e:
    history.pop()
    print(f"Problem: {e}")

user_message = "sorry, my bad. its manoj.pareek@rediff.com"

history.append({
    "role": "user",
    "content": user_message
})

try:
    reply = llm.chat(history, toolSpecs.TOOL_SPECS)
    
    history.append(reply)
    if 'tool_calls' in reply:
        print("Assistant:", reply)
        
        call = reply['tool_calls'][0]
        tool_id = call['id']
        tool_name = call['function']['name']
        tool_args = json.loads(call['function']['arguments'])["email"]

        try: 
            tool_res = json.dumps(tools.find_customer(tool_args))
            # tool_res = tools[tool_name](tool_args)
            print("tool res===", tool_res)
        except tools.ToolError as e:
            tool_res = str(e)
            print('problem==', e)

        history.append({'role': 'tool', 'tool_call_id': tool_id, 'content': tool_res})

except llm.LLMError as e:
    history.pop()
    print(f"Problem: {e}")

try:
    reply = llm.chat(history, toolSpecs.TOOL_SPECS)

    history.append(reply)

    print("Assistant:", reply['content'])

except llm.LLMError as e:
    history.pop()
    print(f"Problem: {e}")


print("\nComplete conversation history:")
print(history)

# 'tool_calls': 
# [
# {
# 'id': 'fc_2531af91-9f69-4f38-a5c0-97845ecd20c9', 
# 'type': 'function', 
# 'function': {'name': 'find_customer', 'arguments': '{"email":"manoj@gmail.com"}'}
# }
# ]
