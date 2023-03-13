import json


def pretty_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=4)

def shorten_str(json_str: str) -> str:
    if len(json_str) > 2000:
        return f"{json_str[:2001]}\n..."
    else:
        return json_str