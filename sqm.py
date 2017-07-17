# tsl2591 SQM reader
# loosely based on https://github.com/jvoight0205/SQM/blob/master/SQM/SQM.ino

from tsl2591.read_tsl import *
import math
import traceback
import numpy

class SQM:
    CALIBRATION_CONSTANT = 13.761
    #CALIBRATION_CONSTANT = 0
    CALIBRATION_LINEAR = 1

    def __init__(self, avg_readings = 10):
        self.device = Tsl2591(integration=INTEGRATIONTIME_600MS)
        self.avg_readings = avg_readings
        self.settings = [
            (GAIN_MAX, 9876.0),
            (GAIN_HIGH, 428.0),
            (GAIN_MED, 25.0),
            (GAIN_LOW, 1.0)
        ]

    def read_median_sqm(self, readings=10):
        readings = [self.read_raw() for n in range(0, readings)]
        sqm_calibrated_values = [self.sqm(reading, calibration=SQM.CALIBRATION_CONSTANT) for reading in readings]
        return numpy.median(sqm_calibrated_values)

    def sqm(self, reading, calibration=0):
        return calibration - 2.5 * math.log10( reading[0] - reading[1])

    def read_raw(self):
        for setting in self.settings:
            try:
                return tuple([x / setting[1] for x in self.__raw_scaled(setting)])
            except OverflowError as e:
                if setting[0] == GAIN_LOW:
                    raise e

    def __raw_scaled(self, setting):
        self.device.set_gain(setting[0])
        reading = self.device.get_full_luminosity()
        if 0xFFFF in reading:
            raise OverflowError('Gain too high')


