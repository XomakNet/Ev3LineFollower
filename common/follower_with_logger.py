from collections import namedtuple

import time

from common.data_logger import DataLogger
from common.follower import Follower

__author__ = 'Xomak'


class SensorPack:
    def get_columns(self):
        pass

    def get_values(self, follower):
        pass


class TwoSonarsPack(SensorPack):
    XYUltrasonicSensors = namedtuple("XYUltasonicSensors", ["x_sensor", "y_sensor"])

    def __init__(self, sensors):
        self.sensors = sensors

    def get_columns(self):
        return ['time', 'x_dst', 'y_dst', 'left_speed', 'right_speed']

    def get_values(self, follower):
        return [time.time(),
                self.sensors.x_sensor.distance_centimeters,
                self.sensors.y_sensor.distance_centimeters,
                follower.left_speed,
                follower.right_speed]


class SonarAndGyroPack(SensorPack):

    def __init__(self, sonar, gyro):
        self.gyro = gyro
        self.sonar = sonar

    def get_columns(self):
        return ['time', 'distance', 'angle', 'left_speed', 'right_speed']

    def get_values(self, follower):
        return [time.time(),
                self.sonar.distance_centimeters,
                self.gyro.angle,
                follower.left_speed,
                follower.right_speed]


class FollowerWithLogger(Follower):
    def __init__(self, right_motor, left_motor, line_detector, sensors_pack, log_path, pid_and_speed_file,
                 update_pid=False):
        super().__init__(right_motor, left_motor, line_detector, pid_and_speed_file, update_pid)
        self.sensors_pack = sensors_pack
        self.logger = DataLogger(sensors_pack.get_columns(), log_path)

    def on_stop(self):
        self.logger.close()

    def control_cycle(self):
        super().control_cycle()
        self.logger.put_values(self.sensors_pack.get_values(self))