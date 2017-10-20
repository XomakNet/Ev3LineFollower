import json
import time

import ev3dev.ev3 as ev3

__author__ = 'Xomak'


def get_json_from_file(file):
    with open(file) as f:
        raw_json = f.read()
        return json.loads(raw_json)


def wait_button():
    buttons = ev3.Button()
    while 'enter' not in buttons.buttons_pressed:
        time.sleep(0.1)
