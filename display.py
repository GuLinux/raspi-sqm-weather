import time
from luma.core.render import canvas
from PIL import ImageFont

class Display:
    def __init__(self, device, logger):
        self.device = device
        self.shown = {}
        self.message = {}
        self.__current_line = 0
        self.__contrast = None
        self.logger = logger

    def set_weather(self, weather_data, render=True):
        if weather_data:
            self.message.update(weather_data)
            if render:
                self.render()

    def set_sqm(self, sqm, render=True):
        if sqm:
            self.message['sqm'] = sqm
            if render:
                self.render()

    def clear(self):
        self.device.clear()
        self.device.hide()

    def render(self, contrast=None):
        self.message['time'] = time.strftime('%H:%M', time.gmtime())
        if self.message != self.shown:
            with canvas(self.device) as draw:
                # draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                self.__draw_line('time', 'time: {} UTC', '{}', draw, first=True)
                self.__draw_line('temp_degrees', u'temp: {}\u00B0C', '{:.3f}', draw)
                self.__draw_line('hPa', u'press.: {} hPa', '{:.3f}', draw)
                self.__draw_line('humidity', u'humidity: {}%', '{:.3f}', draw)
                self.__draw_line('sqm', u'sqm: {}', '{:.3f}', draw)
            self.shown = self.message.copy()
        if contrast is not None and self.__contrast != contrast:
            self.device.contrast(contrast)
            self.__contrast = contrast
            self.logger.debug('Setting contrast to %d', contrast)
        self.device.show()

    def __draw_line(self, keyword, format_string, format_num, draw, first=False):
        font = ImageFont.truetype('DejaVuSans.ttf', 11)
        # font = ImageFont.truetype('DejaVuSerif.ttf', 9)
        if first:
            self.__current_line = 0
       
        if keyword in self.message:
            try:
                value = format_num.format(self.message[keyword])
            except ValueError:
                value = self.message[keyword]

            message = format_string.format(value)
            x = 0
            y = 0 + (self.__current_line * font.getsize(message)[1])
 
            draw.text((x, y), message, fill='white', font=font)
            self.__current_line += 1

