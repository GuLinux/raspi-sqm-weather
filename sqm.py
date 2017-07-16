# tsl2591 SQM reader
# loosely based on https://github.com/jvoight0205/SQM/blob/master/SQM/SQM.ino

from tsl2591.read_tsl import *
import math

class SQM:
    def __init__(self, avg_readings = 5):
        self.device = Tsl2591(integration=INTEGRATIONTIME_600MS)
        self.avg_readings = avg_readings
        self.settings = [
            (GAIN_MAX, 9876.0),
            (GAIN_HIGH, 428.0),
            (GAIN_MED, 25.0),
            (GAIN_LOW, 1.0)
        ]

    def read(self):
        for setting in self.settings:
            try:
                readings = [self.__get_sqm(setting) for i in range(0, self.avg_readings)]
                avg = reduce(lambda a, b: a+b, readings) / len(readings)
                #sqm = -1.085736205 * math.log(0.925925925 * math.pow(10,-5.)*avg);
                sqm = -1.09482135 * math.log(0.925925925 * math.pow(10,-5.)*avg)
                return sqm
            except OverflowError:
                pass
        return None



    def __get_sqm(self, setting):
        self.device.set_gain(setting[0])
        reading = self.device.get_full_luminosity()
        if 0xFFFF in reading:
            raise OverflowError('Gain too high')
        visible = reading[0] - reading[1]
        adjustedVisible = visible / setting[1]
        return adjustedVisible

