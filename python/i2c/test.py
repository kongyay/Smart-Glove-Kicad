#!/usr/bin/python

from time import sleep

from lsm6ds33 import LSM6DS33
from lis3mdl import LIS3MDL

imu = LSM6DS33()
imu.enableLSM()

magnet = LIS3MDL()
magnet.enableLIS()

while True:
    print "Gyro:", imu.getGyroscopeRaw()
    print "Accelerometer:", imu.getAccelerometerRaw()
    print "Magnet:", magnet.getMagnetometerRaw()
    sleep(0.2)
    sleep(0.1)
