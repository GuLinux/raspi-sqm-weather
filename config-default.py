# Weather
from Adafruit_BME280 import *

weather_sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

# Display
from luma.core.interface.serial import spi, i2c
from luma.oled.device import ssd1306

# display_serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=25)
display_serial = i2c(port=1, address=0x3C)
display_device = ssd1306(display_serial)

# light sensor
from tsl2591.read_tsl import *

light_sensor = Tsl2591(integration=INTEGRATIONTIME_600MS)
light_sensor_config = {
    'channels': 2,
    'gain_settings': [
            (GAIN_MAX, 9876.0),
            (GAIN_HIGH, 428.0),
            (GAIN_MED, 25.0),
            (GAIN_LOW, 1.0)
    ]
}

import os

csv_logfile = os.path.join(os.environ['HOME'], 'sqm-weather.csv')

read_weather_every = 30
read_sqm_every = 60 * 1

