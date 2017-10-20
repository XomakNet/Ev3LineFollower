#!/usr/bin/env python3
from utils import get_color

__author__ = 'Xomak'

import ev3dev.ev3 as ev3
import time
import json

speed_bounds = [0, 960]
update_interval = 100

def get_calibration():
    with open("calibration.json") as f:
        raw_json = f.read()
        return json.loads(raw_json)

def get_pid():
    with open("pid.json") as f:
        raw_json = f.read()
        return json.loads(raw_json)

def limit_speed(speed):
    if speed < speed_bounds[0]:
        speed = speed_bounds[0]
    if speed > speed_bounds[1]:
        speed = speed_bounds[1]
    return speed



#base_speed = 960


color_sensor = ev3.ColorSensor()
motor_b = ev3.LargeMotor('outB')
motor_c = ev3.LargeMotor('outC')
calibration = get_calibration()
mean = abs(calibration['line'] - calibration['terrain'])/2
inversed = calibration['line'] < calibration['terrain']

previous_error = 0
integrated = 0
buttons = ev3.Button()

cycles = 0
try:
    while True:
        try:
            pid_params = get_pid()
        except Exception:
            pass

        sensor_value = get_color(color_sensor)
        error = sensor_value - mean

        proportional = error
        derivative = error - previous_error
        integrator = integrated + error

        delta = pid_params['p'] * proportional + pid_params['d'] * derivative + pid_params['i'] * integrator
        if inversed:
            delta = -delta

        motor_b.run_forever(speed_sp=limit_speed(pid_params['speed'] + delta))
        motor_c.run_forever(speed_sp=limit_speed(pid_params['speed'] - delta))
        #time.sleep(0.01)

        if 'enter' in buttons.buttons_pressed:
            break
finally:
    motor_c.run_forever(speed_sp=0)
    motor_b.run_forever(speed_sp=0)