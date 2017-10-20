__author__ = 'Xomak'


class LineDetector:

    @staticmethod
    def get_color(color_sensor):
        return color_sensor.reflected_light_intensity

    def get_error(self):
        pass


class OneSensorLineDetector(LineDetector):

    def __init__(self, sensor, calibration):
        self.sensor = sensor
        self.mean = None
        self.inversed = False
        self.set_calibration(calibration)

    def set_calibration(self, calibration):
        self.mean = abs(calibration['line'] - calibration['terrain']) / 2
        self.inversed = calibration['line'] < calibration['terrain']

    def get_error(self):
        sensor_value = self.get_color(self.sensor)
        error = sensor_value - self.mean
        if self.inversed:
            error = -error
        return error


class TwoSensorsLineDetector(LineDetector):

    def __init__(self, left_sensor, right_sensor, calibration):
        self.sensors = {'left': left_sensor, 'right': right_sensor}
        self.calibration = None
        self.mean = None
        self.inversed = False
        self.set_calibration(calibration)

    def set_calibration(self, calibration):
        self.calibration = calibration
        self.inversed = calibration['line'] < calibration['terrain']

    def _sensor_error(self, sensor):
        target_value = self.calibration['{}_on_line'.format(sensor)]
        return self.get_color(self.sensors[sensor]) - target_value

    def get_error(self):
        left_sensor_error = self._sensor_error('left')
        right_sensor_error = self._sensor_error('right')

        if abs(left_sensor_error) > abs(right_sensor_error):
            error = -abs(left_sensor_error)
        else:
            error = abs(right_sensor_error)

        if self.inversed:
            error = -error

        return error


