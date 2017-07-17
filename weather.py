class WeatherSensor:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self):
        return {
            'temp_degrees': self.sensor.read_temperature(),
            'hPa': self.sensor.read_pressure() / 100,
            'humidity': self.sensor.read_humidity(),
        }

