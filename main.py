from openai import OpenAI
import json
import sys

# Using Gemini LLM through OpenAI SDK
client = OpenAI(
    api_key="GEMINI-API-KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

system_prompt = ""
with open("system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

if len(system_prompt) == 0:
    sys.exit()

query = ''


# Implementation of Chain Of Thought (CoT) based CLI Chatbot using LLM model
while(True):

    query = input("👉 How may I assist you today? ")

    if(query == 'exit'):
        print('Thank you! Have a good time.')
        sys.exit()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query},
    ]

    while True:

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            response_format={"type": "json_object"},
            messages=messages,
        )

        json_res = json.loads(response.choices[0].message.content)
        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        if json_res.get("step") == "START":
            print(f"\n🚀 {json_res.get('content')}\n")

        elif json_res.get("step") == "PLAN":
            print(f"💡 {json_res.get('content')}\n")

        elif json_res.get("step") == "RESULT":
            print(f"🔥 {json_res.get('content')}\n")
            break
