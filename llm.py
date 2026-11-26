import os
from dotenv import load_dotenv
import requests
import time
import tool_specs as tools

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

url= "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization" : f"Bearer {groq_key}"}


class LLMError(Exception):
    pass


def chat(messages, tools):
    body = {"model": "openai/gpt-oss-20b",
        "messages": messages,
        "tools": tools
        }
    for attempt in range(3):
        try:
            response = requests.post(url=url, headers=headers, json=body, timeout=30)
        except requests.exceptions.RequestException as e:
            if attempt == 2:
                raise LLMError(f"network error: {e}")
            time.sleep(2)
            continue

        if response.status_code >= 500 or response.status_code == 429:
            if attempt == 2:
                raise LLMError(f"server error: status code = {response.status_code}, response = {response.text}")
            time.sleep(2)
            continue
        else:
            if response.status_code != 200:
                raise LLMError(f"status code = {response.status_code}, response = {response.text}")
        
    
        data = response.json()
        return data['choices'][0]['message']


history = []

user_message = "Hi, my name is Manoj"

history.append({
    "role": "user",
    "content": user_message
})

try:
    reply = chat(history, tools.TOOL_SPECS)

    history.append(reply)

    print("Assistant:", reply)

except LLMError as e:
    history.pop()
    print(f"Problem: {e}")


user_message = "could you use my mail: manoj@gmail.com and give me all my details"

history.append({
    "role": "user",
    "content": user_message
})

try:
    reply = chat(history, tools.TOOL_SPECS)
    
    history.append(reply)
    print("Assistant:", reply)


except LLMError as e:
    history.pop()
    print(f"Problem: {e}")


print("\nComplete conversation history:")
print(history)

# (.venv) PS C:\Users\jagan\Projects\100days\harness_practice> python llm.py
# Assistant: {'role': 'assistant', 'content': 'Hello Manoj! 👋 How can I help you today? If you’d like me to retrieve your account details or check your order status, just let me know your email address and I’ll pull up your information. If there’s anything else you need—product advice, support, or general questions—feel free to ask!', 'reasoning': 'We need to respond politely, greet Manoj. Ask what they need. Possibly ask for email to get details.'}
# Assistant: {'role': 'assistant', 'reasoning': 'We must call the find_customer function.', 'tool_calls': [{'id': 'fc_2531af91-9f69-4f38-a5c0-97845ecd20c9', 'type': 'function', 'function': {'name': 'find_customer', 'arguments': '{"email":"manoj@gmail.com"}'}}]}

# Complete conversation history:
# [{'role': 'user', 'content': 'Hi, my name is Manoj'}, {'role': 'assistant', 'content': 'Hello Manoj! 👋 How can I help you today? If you’d like me to retrieve your account detailsor check your order status, just let me know your email address and I’ll pull up your information. If there’s anything else you need—product advice, support, or general questions—feel free to ask!', 'reasoning': 'We need to respond politely, greet Manoj. Ask what they need. Possibly ask for email to get details.'}, {'role': 'user', 'content': 'could you usemy mail: manoj@gmail.com and give me all my details'}, {'role': 'assistant', 'reasoning': 'We must call the find_customer function.', 'tool_calls': [{'id': 'fc_2531af91-9f69-4f38-a5c0-97845ecd20c9', 'type': 'function', 'function': {'name': 'find_customer', 'arguments': '{"email":"manoj@gmail.com"}'}}]}]
