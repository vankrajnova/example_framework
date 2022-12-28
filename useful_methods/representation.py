import json


def json_as_pretty_str(my_json):
    return json.dumps(my_json, ensure_ascii=False, indent=3)
