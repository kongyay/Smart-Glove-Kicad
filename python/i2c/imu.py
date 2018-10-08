#!/usr/bin/python

from datetime import datetime
from time import sleep
from altimu import AltIMU
from lis3mdl import LIS3MDL

imu = AltIMU()
imu.enable()
mag = LIS3MDL()
mag.enableLIS(magnetometer=True,temperature=False)

imu.calibrateGyroAngles()

#for x in range(1000):
#    startTime = datetime.now()
#    angles = imu.trackGyroAngles(deltaT = 0.0002)

#print angles

def run_imu(start):
    stop = datetime.now() - start
    deltaT = stop.microseconds/1000000.0
    #print " "
    #print "Loop:", deltaT
    #print "Accel:", imu.getAccelerometerAngles()
    #print "Gyro:", imu.trackGyroAngles(deltaT = deltaT)
    dataTuple = imu.getAccelerometerAngles()
    dataTuple.extend(imu.getGyroRotationRates())
    dataTuple.extend(mag.getMagnetometerRaw())
    return dataTuple
