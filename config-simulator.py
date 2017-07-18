logger = logging.getLogger('sqm-weather')
logger.setLevel(logging.DEBUG)



# Weather
class WeatherSimulator:
    def read_temperature(self):
        return 34

    def read_pressure(self):
        return 100

    def read_humidity(self):
        return 80

weather_sensor = WeatherSimulator()

# Display
from luma.emulator.device import capture
display_device = capture()

# light sensor
class LightSensorSimulator:
    def set_gain(self, gain):
        self.gain = gain

    def get_full_luminosity(self):
        return 1234 * self.gain
 

light_sensor = LightSensorSimulator()
light_sensor_config = {
    'channels': 1,
    'gain_settings': [
            (10, 10),
            (5, 5),
            (1, 1.0)
    ]
}
sqm_readings = 2

import os
csv_logfile = os.path.join(os.environ['HOME'], 'sqm-weather.csv')

read_weather_every = 30
read_sqm_every = 60 * 1

