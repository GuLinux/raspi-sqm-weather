import time
from luma.core.render import canvas

class Display:
    def __init__(self, device):
        self.device = device
        self.shown = {}
        self.message = {}
        self.__current_line = 0

    def set_weather(self, weather_data):
        self.message.update(weather_data)
        self.render()

    def set_sqm(self, sqm):
        self.message['sqm'] = sqm
        self.render()

    def clear(self):
        self.device.clear()
        #self.device.show()
        self.device.hide()

    def render(self):
        self.message['time'] = time.strftime('%H:%M', time.gmtime())
        if self.message != self.shown:
            with canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                self.__draw_line('time', 'time: {} UTC', draw, first=True)
                self.__draw_line('temp_degrees', u'temp: {:.3f}\u00B0C', draw)
                self.__draw_line('hPa', u'press.: {:.3f} hPa', draw)
                self.__draw_line('humidity', u'humidity: {:.3f}%', draw)
                self.__draw_line('sqm', u'sqm: {:.3f}', draw)
            self.shown = self.message.copy()

    def __draw_line(self, keyword, format_string, draw, first=False):
        font_size = 10
        if first:
            self.__current_line = 0
        x = 3
        y = 1 + (self.__current_line * font_size)
        
        if keyword in self.message:
            draw.text((x, y), format_string.format(self.message[keyword]), fill='white')
            self.__current_line += 1

