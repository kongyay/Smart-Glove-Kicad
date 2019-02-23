import time
import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont
from datetime import datetime

class Oled(object):
	def __init__(self):
		# # Set up
		self.serial = i2c(port=0, address=0x3C)
		self.device = ssd1306(self.serial)
		self.device.clear()

		# # Variables
		self.numRow = 5
		self.fonts = {
			'th': self.make_font('THSarabunNew.ttf', 15),
			'big': self.make_font('THSarabunNew.ttf', 40),
			# 'fa':self.make_font('FontAwesome.ttf', 15),
		}
		self.texts = ['' for i in range(self.numRow)]
		self.info = {
			'ip': '',
			'dt': datetime.now(),
			'sensor': [False for i in range(5)]
		}

	def write_row(self, row=0, text="No Text..", font="th"):
		if self.texts[row] == text:
			return

		self.texts[row] = text
		with canvas(self.device) as draw:
			for i in range(self.numRow):
				draw.text(
					(0, 0 if i == 0 else 5+10*i), self.texts[i], font=self.fonts[font], fill="white")

	def drawPixel(self, pixels):
		with canvas(self.device) as draw:
			for y in range(0, 64):
				for x in range(0, 128):
					index = y*128+x
					if len(pixels) <= index:
						return
					draw.point((x, y), fill=("white" if pixels[index] == "1" else "black"))

	def init_oled(self):
		start_text = "Glove to Gesture"
		with canvas(self.device) as draw:
			w, h = draw.textsize(
				text=start_text, font=self.fonts['th'])
			left = (self.device.width - w) / 2
			top = (self.device.height - h) / 2
			draw.text((left, top), text=start_text,
				  font=self.fonts['th'], fill="white")

	def make_font(self, name, size):
		font_path = os.path.abspath(os.path.join(
			os.path.dirname(__file__), 'fonts', name))
		return ImageFont.truetype(font_path, size)

	def set_info(self, key, data):
		self.info[key] = data

	def show_clock(self):
		interface = [
			'IP: ' + self.info['ip'],
			'DATE: '+self.info['dt'].strftime("%a, %d %b %Y"),
		]

		with canvas(self.device) as draw:
			for i in range(len(interface)):
				draw.text(
					(0, 0 if i == 0 else 3+10*i), interface[i], font=self.fonts['th'], fill="white")

			draw.text((0, 25), self.info['dt'].strftime(
				"%H:%M"), font=self.fonts['big'], fill="white")


class NullOled(object):
	def __init__(self):
		return

	def write_row(self, row=0, text="No Text.."):
		print('NULLOLED: Write Row')
		return

	def init_oled(self):
		print('NULLOLED: Init OLED')
		return

	def make_font(self, name, size):
		print('NULLOLED: Make font')
		return

	def set_info(self, key, data):
		print('NULLOLED: Set Info')
		return

	def show_clock(self):
		print('NULLOLED: Show Clock')
		return

	def drawPixel(self, pixels):
		print('NULLOLED: Draw Pixel')
		return


try:
	display = Oled()
	display.write_row(text="Starting....", row=0)
	display.write_row(text="กำลังเริ่มต้น...", row=1)
	print("Init OLED")
except (Exception) as err: 
	print("Error Init OLED:", err)
	display = NullOled()
