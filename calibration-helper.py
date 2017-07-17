#!/usr/bin/python
import time, datetime

from weather import WeatherSensor
from sqm import SQM
import config

def main():
    weather = WeatherSensor(config.weather_sensor)
    sqm_reader = SQM(config.light_sensor, config.light_sensor_config)

    csv_file = open('calibration.csv', 'w')
    csv_file.write('timestamp,datetime_utc,t_celsius, reading_fs, reading_ir, sqm\n')

    while(True):
        weather_data, sqm_data = None, None
        try:
            weather_data = weather.read()
            sqm_data = sqm_reader.read_raw()
        except:
            continue

        if not weather_data or not sqm_data:
            continue

        sqm_uncalibrated = sqm_reader.sqm(sqm_data)
        full_spectrum = sqm_data[0] if type(sqm_data) is tuple else sqm_data
        ir_value = sqm_data[1] if type(sqm_data) is tuple else -1

        csv_file.write('{timestamp},{datetime_utc},{t_celsius},{reading_fs},{reading_ir},{sqm}\n'.format(
            timestamp=time.time(),
            datetime_utc=datetime.datetime.utcnow().isoformat(),
            t_celsius=weather_data['temp_degrees'],
            reading_fs=full_spectrum,
            reading_ir=ir_value,
            sqm=sqm_uncalibrated
        ))
               

if __name__ == "__main__":
    main()

