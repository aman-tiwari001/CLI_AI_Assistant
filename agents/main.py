from openai import OpenAI
import tools
import json
import sys
import custom_types

client = OpenAI(
    api_key="GEMINI-API-KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

TOOLS = {"get_weather": tools.get_weather}

system_prompt = None
with open("system.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

if system_prompt == None:
    print("No System Prompt found! exiting...")
    sys.exit()

# ChatML Prompting
messages = [{"role": "system", "content": system_prompt}]

while True:
    query = input("👉 What's on your mind? ")

    if query == "exit":
        print("Thank you! have a good time 😊")
        sys.exit()

    messages.append({"role": "user", "content": query})

    deviation_count = 0

    while True:
        tools.write(json.dumps(messages))
        response = client.chat.completions.parse(
            model="gemini-2.5-flash",
            response_format=custom_types.OutputFormat,
            messages=messages,
        )

        # parsed_res = json.loads(response.choices[0].message.content)
        parsed_res = response.choices[0].message.parsed

        deviated = tools.guard_rail(parsed_res, messages, "step")
        if deviated:
            print("🚨 Model deviated. Guardrails activated!\n")
            deviation_count += 1
            if deviation_count > 3:
                break
            continue

        messages.append(
            {"role": "assistant", "content": response.choices[0].message.content}
        )

        if parsed_res.step == "START":
            print(f"\n🚀 START : {parsed_res.content}\n")

        elif parsed_res.step == "PLAN":
            print(f"🧠 PLAN : {parsed_res.content}\n")

        elif parsed_res.step == "TOOL_CALL":
            print(f"🧠 TOOL_CALL : {parsed_res.content}\n")
            tool_name = parsed_res.tool_name
            tool_input = parsed_res.tool_input
            tool_output = TOOLS.get(tool_name)(tool_input)

            messages.append(
                {
                    "role": "developer",
                    "content": json.dumps(
                        {
                            "step": "TOOL_OUTPUT",
                            "tool_name": tool_name,
                            "tool_input": tool_input,
                            "tool_output": tool_output,
                        }
                    ),
                }
            )

        elif parsed_res.step == "TOOL_OUTPUT":
            print(f"🔨 TOOL_OUTPUT : {parsed_res.tool_output}\n")

        elif parsed_res.step == "RESULT":
            print(f"🤖 RESULT : {parsed_res.content}\n")
            break
