#!/usr/bin/python
import time

from weather import WeatherSensor
from sqm import SQM

def main():
    weather = WeatherSensor()
    sqm_reader = SQM()

    csv_file = open(csv_file, 'w')
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
        csv_file.write('{timestamp},{datetime_utc},{t_celsius},{reading_fs},{reading_ir},{sqm}\n'.format(
            timestamp=time.time(),
            datetime_utc=datetime.datetime.utcnow().isoformat(),
            weather_data['temp_degrees'],
            sqm_data[0],
            sqm_data[1],
            sqm_uncalibrated
        ))
               

if __name__ == "__main__":
    main()

