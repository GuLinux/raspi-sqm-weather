from Adafruit_BME280 import *

class WeatherSensor:
    def __init__(self):
        self.sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

    def read(self):
        return {
            'temp_degrees': self.sensor.read_temperature(),
            'hPa': self.sensor.read_pressure() / 100,
            'humidity': self.sensor.read_humidity(),
        }

