import os
from dotenv import load_dotenv
import requests
import time
import tool_specs as toolSpecs
import json
import tools

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

url= "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization" : f"Bearer {groq_key}"}


class LLMError(Exception):
    pass


def chat(messages, tool_specs):
    body = {"model": "openai/gpt-oss-20b",
        "messages": messages,
        "tools": tool_specs
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

