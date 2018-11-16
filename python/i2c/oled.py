import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

class Oled(object):
        def __init__(self):
                self.serial = i2c(port=0, address=0x3C)
                self.device = ssd1306(self.serial)
                self.device.clear()


        def write_row(self, row=0, text="No Text.."):
                with canvas(self.device) as draw:
                        draw.text((0, 0 if row == 0 else 5+10*row), text, fill="white")


        def init_oled(self):
                with canvas(self.device) as draw:
                        draw.text((0, 0), "Glove to Gesture", fill="white")


        def write_all(self, texts=[]):
                with canvas(self.device) as draw:
                        for i in range(len(texts)):
                                draw.text((0, 0 if i == 0 else 5+10*i), texts[i], fill="white")

try:
        display = Oled()
        display.write_row(text="Starting....")
        print("Init OLED")
except (Exception):
        print("Error Init OLED")
        display = None