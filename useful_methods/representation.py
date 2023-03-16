import json

from model import User, Position, Orgunit


def pretty_json(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=4)

def shorten_str(json_str: str) -> str:
    if len(json_str) > 2000:
        return f"{json_str[:2001]}\n..."
    else:
        return json_str

def pretty_str(text, obj, indent=0):
    if text == '':
        lines = []
    else:
        lines = ['']
    if type(obj) == User:
        lines.append(text + '{')
        lines.append(f'\taccount_name: {str(obj.info.account_name)},')
        lines.append(f'\toid: {str(obj.info.oid)},')
        if obj.info.hr_id is not None:
            lines.append(f'\thr_id: {str(obj.info.hr_id)}, emp_hr_id: {str(obj.employment.emp_hr_id)}')
        lines.append(f'\tposition: {str(obj.employment.position.name)},')
        lines.append(f'\torgunit_chain: {str(obj.employment.position.get_parent_chain_as_lines())},')
        lines.append('}')
    elif type(obj) == Position:
        lines.append(text + '{')
        lines.append(f'\tposition_name: {str(obj.name)},')
        lines.append(f'\toid: {str(obj.oid)},')
        lines.append(f'\torgunit_chain: {str(obj.get_parent_chain_as_lines())},')
        lines.append('}')
    elif type(obj) == Orgunit:
        lines.append(text + '{')
        lines.append(f'\torg_unit_name: {str(obj.name)},')
        lines.append(f'\toid: {str(obj.oid)},')
        lines.append(f'\torgunit_chain: {str(obj.get_parent_chain_as_lines())},')
        lines.append('}')
    else:
        lines.append(text + str(obj))
    lines = ['\t' * indent + x for x in lines]
    result = '\n'.join(lines)
    return result.replace('\t', '   ')


def pretty_print(name, obj, indent=0):
    print(pretty_str(name, obj, indent))