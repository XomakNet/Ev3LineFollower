#!/usr/bin/env python3
import time

import ev3dev.ev3 as ev3

from common.follower_with_logger import FollowerWithLogger, TwoSonarsPack, SonarAndGyroPack
from common.line_detectors import TwoSensorsLineDetector
from common.utils import get_json_from_file

__author__ = 'Xomak'


left_color_sensor = ev3.ColorSensor(address='in1')
right_color_sensor = ev3.ColorSensor(address='in3')
left_motor = ev3.LargeMotor('outB')
right_motor = ev3.LargeMotor('outC')
calibration = get_json_from_file('data/calibration_two_sensors.json')

line_detector = TwoSensorsLineDetector(left_color_sensor, right_color_sensor, calibration)

sonar_gyro = SonarAndGyroPack(ev3.UltrasonicSensor('in2'), ev3.GyroSensor('in4'))

follower = FollowerWithLogger(right_motor, left_motor, line_detector, sonar_gyro, 'logs/log.csv',
                              'data/pid_and_speed_2.json', update_pid=True)
follower.follow()



