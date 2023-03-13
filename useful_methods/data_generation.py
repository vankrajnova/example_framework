from pathlib import Path
import json
import random
import time


def _get_config():
    root = Path(__file__).parent
    config = '../env_config.json'
    config_path = (root / config).resolve()
    with open(config_path, encoding='utf-8') as f:
        config = json.load(f)
        return config


def _get_ou_number():
    config = _get_config()
    ou = config["config"]["ad_org_unit"]
    ou_number = ou.lower().replace('autotest', '')
    return ou_number

def convert_numbers_to_letters(numbers_as_str: str):
    pairs = {
        "0": "a",
        "1": "b",
        "2": "c",
        "3": "d",
        "4": "e",
        "5": "f",
        "6": "g",
        "7": "h",
        "8": "i",
        "9": "k",
    }
    s = ''
    for number_as_str in numbers_as_str:
        s += pairs[number_as_str]
    l = []
    for letter in s:
        l.append(letter)
    random.shuffle(l)
    suffix = ''.join(l)
    return suffix

def make_unique_suffix():
    suffix = f"{_get_ou_number()}{''.join(random.choice('qwertyuiopasdfghjklzxcvbnm') for i in range(1))}"
    suffix += convert_numbers_to_letters(str(round(time.time() * 1000)))
    return suffix

def make_unique_name(prefix="A"):
    return f'{prefix}{make_unique_suffix()}'
