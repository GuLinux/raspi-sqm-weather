import os
import time
import datetime

class CSVLogger:
    def __init__(self, csv_file):
        if os.path.isfile(csv_file):
            self.csv_file = open(csv_file, 'a')
        else:
            self.csv_file = open(csv_file, 'w')
            self.csv_file.write('timestamp,datetime_utc,t_celsius,humidity,hPa,sqm\n')
        self.csv_file.flush()

    def line(self, t_celsius, humidity, hPa, sqm):
        self.csv_file.write('{timestamp},{datetime_utc},{t_celsius:.3f},{humidity:.3f},{hPa:.3f}, {sqm:.3f}\n'.format(
               timestamp=time.time(),
               datetime_utc=datetime.datetime.utcnow().isoformat(),
               t_celsius=t_celsius,
               humidity=humidity,
               hPa=hPa,
               sqm=sqm
            )
        )

        self.csv_file.flush()

