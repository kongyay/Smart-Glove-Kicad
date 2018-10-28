import time
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

serial = i2c(port=0, address=0x3C)
device = ssd1306(serial)
device.clear()
 
def write_row(row = 0,text="No Text.."):
    with canvas(device) as draw:
        draw.text((0, 0 if row==0 else 5+10*row), text, fill="white")
    
def init_oled():
    with canvas(device) as draw:
        draw.text((0, 0), "Glove to Gesture", fill="white")

def write_all(texts=[]):
    with canvas(device) as draw:
        for i in range(len(texts)):
            draw.text((0, 0 if i==0 else 5+10*i), texts[i], fill="white")
