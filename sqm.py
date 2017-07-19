# tsl2591 SQM reader
# loosely based on https://github.com/jvoight0205/SQM/blob/master/SQM/SQM.ino


import math
import traceback
import numpy

class SQM:
    CALIBRATION_CONSTANT = 13.761
    #CALIBRATION_CONSTANT = 0
    CALIBRATION_LINEAR = 1

    def __init__(self, config):
        self.light_sensor = config.light_sensor
        self.light_sensor_config = config.light_sensor_config

    def read_median_sqm(self, readings=10):
        readings = [self.read_raw() for n in range(0, readings)]
        sqm_calibrated_pairs = [self.sqm(reading, calibration=SQM.CALIBRATION_CONSTANT) for reading in readings]
        sqm_values = [v[0] for v in sqm_calibrated_pairs]
        sqm_raw_frequencies = [v[1] for v in sqm_calibrated_pairs]

        return numpy.median(sqm_values), numpy.median(sqm_raw_frequencies)

    def sqm(self, reading, calibration=0):
        frequency = reading
        if self.light_sensor_config['channels'] == 2:
            frequency = reading[0] - reading[1]
        return calibration - 2.5 * math.log10(frequency), frequency

    def read_raw(self):
        for gain_setting in self.light_sensor_config['gain_settings']:
            try:
                readings = self.__raw_scaled(gain_setting)
                if type(readings) is tuple:
                    return tuple([x / gain_setting[1] for x in self.__raw_scaled(gain_setting)])
                return readings / gain_setting[1]
            except OverflowError as e:
                if gain_setting[0] == self.light_sensor_config['gain_settings'][-1]:
                    raise e

    def __raw_visible_spectrum(self, value)
        if type(value) is tuple:
            return value[0] - value[1]
        return value

    def __raw_scaled(self, gain_setting):
        self.light_sensor.set_gain(gain_setting[0])
        reading = self.light_sensor.get_full_luminosity()
        if (type(reading) is tuple and 0xFFFF in reading) or 0xFFFF == reading:
            raise OverflowError('Gain too high')
        return reading

