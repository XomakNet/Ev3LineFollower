#!/usr/bin/env python3

import json
import time

import ev3dev.ev3 as ev3

from utils import get_color

__author__ = 'Xomak'

def wait_button():
    buttons = ev3.Button()
    while 'enter' not in buttons.buttons_pressed:
        time.sleep(0.1)

color_sensor = ev3.ColorSensor()


calibration = {}
print("Please, show me the line and press the button...")
wait_button()
calibration['line'] = get_color(color_sensor)
print("Please, show me the terrain and press the button...")
wait_button()
calibration['terrain'] = get_color(color_sensor)

with open("calibration.json", "w") as f:
    f.write(json.dumps(calibration))
