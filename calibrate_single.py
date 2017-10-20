#!/usr/bin/env python3

import json
import time

import ev3dev.ev3 as ev3

from common.line_detectors import LineDetector
from common.utils import wait_button

__author__ = 'Xomak'

color_sensor = ev3.ColorSensor()


calibration = {}
print("Please, show me the line and press the button...")
wait_button()
calibration['line'] = LineDetector.get_color(color_sensor)
print("Please, show me the terrain and press the button...")
wait_button()
calibration['terrain'] = LineDetector.get_color(color_sensor)

with open("calibration.json", "w") as f:
    f.write(json.dumps(calibration))
