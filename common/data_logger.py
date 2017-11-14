import csv

__author__ = 'Xomak'


class DataLogger:

    def __init__(self, columns, filename):
        self.columns = columns
        self.file = open(filename, "w")
        self.csv = csv.writer(self.file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.put_values(columns)

    def put_values(self, values):
        self.csv.writerow(values)

    def close(self):
        self.file.close()