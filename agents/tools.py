import requests


def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    res = requests.get(url)

    if res.status_code == 200:
        normalized = res.text.replace("\u00b0C", " Celsius")
        return f"The weather in {city} is {normalized}"
    else:
        return "Something went wrong!"


def write(content: str):
    with open("msg.txt", "w", encoding="utf-8") as f:
        f.write(content)


def guard_rail(res_object: dict, messages: list, *keys):
    for key in keys:
        if isinstance(res_object, dict) and res_object.get(key) is None:
            messages.append(
                {
                    "role": "developer",
                    "content": "You are not following the output guidelines mentioned in the system prompt. Strictly adhere to this JSON Output format : {'step': 'START' | 'PLAN' | 'TOOL_CALL' | 'TOOL_OUTPUT' | 'RESULT', 'content' : string, 'tool_name'?: string, 'tool_input'?: string, 'tool_output'?: string } ",
                }
            )
            return True

    return False
