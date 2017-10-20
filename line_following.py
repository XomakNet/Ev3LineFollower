#!/usr/bin/env python3
import json

import ev3dev.ev3 as ev3

from common.line_detectors import OneSensorLineDetector
from common.utils import get_json_from_file
from common.pid import PIDRegulator

__author__ = 'Xomak'

speed_bounds = [0, 960]
update_interval = 100
calibration_file = 'calibration.json'
pid_file = 'pid.json'


def limit_speed(speed):
    if speed < speed_bounds[0]:
        speed = speed_bounds[0]
    if speed > speed_bounds[1]:
        speed = speed_bounds[1]
    return speed


color_sensor = ev3.ColorSensor()
motor_b = ev3.LargeMotor('outB')
motor_c = ev3.LargeMotor('outC')
calibration = get_json_from_file(calibration_file)
pid_params = get_json_from_file(pid_file)

buttons = ev3.Button()
pid_regulator = PIDRegulator()
line_detector = OneSensorLineDetector(color_sensor, calibration)

cycles = update_interval
try:
    while True:
        if cycles >= update_interval:
            try:
                pid_params = get_json_from_file(pid_file)
                pid_regulator.p = pid_params['p']
                pid_regulator.i = pid_params['i']
                pid_regulator.d = pid_params['d']
                cycles = 0
            except Exception:
                pass

        error = line_detector.get_error()
        delta = pid_regulator.proceed(error)

        motor_b.run_forever(speed_sp=limit_speed(pid_params['speed'] + delta))
        motor_c.run_forever(speed_sp=limit_speed(pid_params['speed'] - delta))

        if 'enter' in buttons.buttons_pressed:
            break
finally:
    motor_c.run_forever(speed_sp=0)
    motor_b.run_forever(speed_sp=0)
