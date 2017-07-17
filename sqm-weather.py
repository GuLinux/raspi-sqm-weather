#!/usr/bin/python
import time
from display import Display
from weather import WeatherSensor
from sqm import SQM

from csv_logger import CSVLogger
import config
import traceback


def main():
    display = Display(config.display_device)
    weather = WeatherSensor(config.weather_sensor)
    sqm_reader = SQM(config.light_sensor, config.light_sensor_config)

    csv = CSVLogger(config.csv_logfile)

    read_weather_every = 30
    read_sqm_every = 60 * 1

    last_weather_read = 0
    last_sqm_read = 0

    weather_data = None
    sqm_data = None
 

    while True:
        now = time.time()
        if now - last_weather_read > read_weather_every:
            last_weather_read = now
            weather_data = weather.read()

        if now - last_sqm_read > read_sqm_every:
            display.clear()
            try:
                sqm_data = sqm_reader.read_median_sqm()
            except:
                traceback.print_exc()
                sqm_data = None
            last_sqm_read = now
            csv.line(weather_data['temp_degrees'], weather_data['humidity'], weather_data['hPa'], sqm_data)

        display_brightness = 0
        if sqm_data and sqm_data < 8:
            display_brightness = 128
        if sqm_data and sqm_data < 6.5:
            display_brightness = 255

        display.set_weather(weather_data, render=False)
        display.set_sqm(sqm_data, render=False)
        display.render(contrast=display_brightness)
        time.sleep(1)
        

if __name__ == "__main__":
    main()

