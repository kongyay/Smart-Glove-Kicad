import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class Oled(object):
        def __init__(self):
                self.serial = i2c(port=0, address=0x3C)
                self.device = ssd1306(self.serial)
                self.device.clear()
                self.numRow = 6
                self.texts = ['' for i in range(self.numRow)]


        def write_row(self, row=0, text="No Text.."):
                self.texts[row] = text
                with canvas(self.device) as draw:
                        for i in range(self.numRow):
                                draw.text((0, 0 if i == 0 else 5+10*i), self.texts[i], fill="white")


        def init_oled(self):
                with canvas(self.device) as draw:
                        draw.text((0, 0), "Glove to Gesture", fill="white")
class NullOled(object):
        def __init__(self):
                return

        def write_row(self, row=0, text="No Text.."):
                return

        def init_oled(self):
                return
try:
        display = Oled()
        display.write_row(text="Starting....")
        print("Init OLED")
except (Exception) as err:
        print("Error Init OLED:",err)
        display = NullOled()