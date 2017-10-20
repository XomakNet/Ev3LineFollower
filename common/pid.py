__author__ = 'Xomak'


class PIDRegulator:

    def __init__(self, p=0, i=0, d=0, initial_condition=0):
        self.p = p
        self.i = i
        self.d = d
        self._integrated_sum = initial_condition
        self._previous_value = 0

    def proceed(self, value):
        proportional_part = value
        derivative_part = value - self._previous_value
        integrative_part = self._integrated_sum + value
        self._integrated_sum = integrative_part
        self._previous_value = value
        return self.p * proportional_part + self.i * integrative_part + self.d * derivative_part

