import os
import time
import datetime

class CSVLogger:
    def __init__(self, csv_file):
        if os.path.isfile(csv_file):
            self.csv_file = open(csv_file, 'a')
        else:
            self.csv_file = open(csv_file, 'w')
            self.csv_file.write('timestamp,datetime_utc,t_celsius,humidity,hPa,sqm, light_sensor_reading_raw\n')
        self.csv_file.flush()

    def line(self, t_celsius, humidity, hPa, sqm, light_sensor_reading):
        self.csv_file.write('{timestamp},{datetime_utc},{t_celsius},{humidity},{hPa}, {sqm}, {light_sensor_reading}\n'.format(
               timestamp=time.time(),
               datetime_utc=datetime.datetime.utcnow().isoformat(),
               t_celsius=self.__float(t_celsius),
               humidity=self.__float(humidity),
               hPa=self.__float(hPa),
               sqm=self.__float(sqm),
               light_sensor_reading=light_sensor_reading
            )
        )

        self.csv_file.flush()

    def __float(self, number):
        try:
            return '{:.3f}'.format(number)
        except ValueError:
            return 'n/a'

