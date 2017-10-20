__author__ = 'Xomak'


class LineDetector:

    @staticmethod
    def get_color(color_sensor):
        return color_sensor.red

    def get_error(self):
        pass


class OneSensorLineDetector(LineDetector):

    def __init__(self, sensor, calibration):
        self.sensor = sensor
        self.set_calibration(calibration)
        self.mean = None
        self.inversed = False

    def set_calibration(self, calibration):
        self.mean = abs(calibration['line'] - calibration['terrain']) / 2
        self.inversed = calibration['line'] < calibration['terrain']

    def get_error(self):
        sensor_value = self.get_color(self.sensor)
        error = sensor_value - self.mean
        if self.inversed:
            error = -error
        return error


