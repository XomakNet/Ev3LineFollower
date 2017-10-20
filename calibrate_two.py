#!/usr/bin/env python3

import json
import time

import ev3dev.ev3 as ev3

from common.line_detectors import LineDetector
from common.utils import wait_button

__author__ = 'Xomak'

left_color_sensor = ev3.ColorSensor(address='in1')
right_color_sensor = ev3.ColorSensor(address='in2')


calibration = {}
print("Please, show me the line and press the button...")
wait_button()
calibration['line'] = (LineDetector.get_color(left_color_sensor) + LineDetector.get_color(right_color_sensor))/2
print("Please, show me the terrain and press the button...")
wait_button()
calibration['terrain'] = (LineDetector.get_color(left_color_sensor) + LineDetector.get_color(right_color_sensor))/2
print("Please, put me along the line and press the button...")
wait_button()
calibration['left_on_line'] = LineDetector.get_color(left_color_sensor)
calibration['right_on_line'] = LineDetector.get_color(left_color_sensor)

with open("data/calibration_two_sensors.json", "w") as f:
    f.write(json.dumps(calibration))
