#!/usr/bin/env python3

import ev3dev.ev3 as ev3

from common.utils import get_json_from_file
from common.pid import PIDRegulator

__author__ = 'Xomak'


class Follower:

    def __init__(self, right_motor, left_motor, line_detector, pid_and_speed_file, update_pid=False):
        self.speed_bounds = [0, 960]
        self.update_interval = 100
        self.pid_file = pid_and_speed_file
        self.buttons = ev3.Button()
        self.left_speed = None
        self.right_speed = None
        self.pid_regulator = PIDRegulator()
        self.line_detector = line_detector
        self.update_pid_enabled = update_pid
        self.right_motor = right_motor
        self.left_motor = left_motor
        self.pid_and_speed_params = None
        self._update_pid_params()

    def _limit_speed(self, speed):
        if speed < self.speed_bounds[0]:
            speed = self.speed_bounds[0]
        if speed > self.speed_bounds[1]:
            speed = self.speed_bounds[1]
        return speed

    def _update_pid_params(self):
        try:
            self.pid_and_speed_params = get_json_from_file(self.pid_file)
            self.pid_regulator.p = self.pid_and_speed_params['p']
            self.pid_regulator.i = self.pid_and_speed_params['i']
            self.pid_regulator.d = self.pid_and_speed_params['d']
        except Exception:
            print("Error reading PID params.")

    def control_cycle(self):
        error = self.line_detector.get_error()
        delta = self.pid_regulator.proceed(error)

        self.left_speed = self._limit_speed(self.pid_and_speed_params['speed'] + delta)
        self.right_speed = self._limit_speed(self.pid_and_speed_params['speed'] - delta)

        self.left_motor.run_forever(speed_sp=self.left_speed)
        self.right_motor.run_forever(speed_sp=self.right_speed)

    def on_stop(self):
        pass

    def follow(self):
        print("Main cycle started...")
        try:
            cycles = 0
            while True:
                if cycles >= self.update_interval and self.update_pid_enabled:
                    self._update_pid_params()
                self.control_cycle()
                if 'enter' in self.buttons.buttons_pressed:
                    break
                cycles += 1
        finally:
            self.right_motor.run_forever(speed_sp=0)
            self.left_motor.run_forever(speed_sp=0)
            self.on_stop()
