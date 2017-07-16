#!/usr/bin/python

import time
from display import Display

from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from weather import WeatherSensor
from sqm import SQM
from csv_logger import CSVLogger

def main():
    serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=25)
    device = ssd1306(serial)
    display = Display(device)
    weather = WeatherSensor()
    sqm_reader = SQM()
    csv = CSVLogger('/home/pi/sqm_weather.csv')

    read_weather_every = 30
    read_sqm_every = 60 * 1

    last_weather_read = 0
    last_sqm_read = 0

    while True:
        weather_data = None
        sqm_data = None
        now = time.time()
        if now - last_weather_read > read_weather_every:
            last_weather_read = now
            weather_data = weather.read()

        if now - last_sqm_read > read_sqm_every:
            display.clear()
            sqm_data = sqm_reader.read()
            last_sqm_read = now
            csv.line(weather_data['temp_degrees'], weather_data['humidity'], weather_data['hPa'], sqm_data)

        display.set_weather(weather_data, render=False)
        display.set_sqm(sqm_data, render=False)
        display.render()
        time.sleep(1)
        

if __name__ == "__main__":
    main()

