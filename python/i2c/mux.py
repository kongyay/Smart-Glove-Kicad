#!/usr/bin/python
# TCA9548A I2C multiplexer
# I2C Address: 70 through 77
# Channel: 0 - 7

from smbus2 import SMBus

# class for the I2C switch----------------------------------------------------


class I2C_SW(object):
    # init________________________________________________________________________
    def __init__(self, name, address, bus_nr):
        self.name = name
        self.address = address
        self.bus_nr = bus_nr
        self.bus = SMBus(bus_nr)

# Change to i2c channel 0..7__________________________________________________
    def channel(self, channel):
        self.bus.write_byte(self.address, 2**channel)

# block all channels read only the main I2c ( on which is the address SW)_____
    def reset(self):
        self.bus.write_byte(self.address, 0)
        print (self.name, ' ', 'Switch reset')

# read all 8 channels__________________________________________________________
    def all(self):
        self.bus.write_byte(self.address, 0xff)
        print (self.name, ' ', 'Switch read all lines')

# define the usual sensor 0X70 bus 1__________________________________________


SW = I2C_SW('I2C switch 0', 0x70, 0)
# SW._all()
# SW.reset()
# to enable a channel : SW._chn(channel number - here 0 to 7)
# check with i2cdetect y -1 (if bus_nr=1)
