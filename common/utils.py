import json

__author__ = 'Xomak'


def get_json_from_file(file):
    with open(file) as f:
        raw_json = f.read()
        return json.loads(raw_json)
