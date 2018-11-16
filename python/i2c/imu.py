#!/usr/bin/python

from datetime import datetime
from time import sleep
from altimu import AltIMU
from lis3mdl import LIS3MDL


class IMU(object):
    def __init__(self, channel=0, name=None):
        self.channel = channel
        self.name = name or channel
        self.imu = AltIMU()
        self.mag = LIS3MDL()

        self.imu.enable()
        self.mag.enableLIS(magnetometer=True)

        self.imu.calibrateGyroAngles()

        # TEST
        # for x in range(1000):
        #    startTime = datetime.now()
        #    angles = imu.trackGyroAngles(deltaT = 0.0002)

        #print angles

    def enable(self):
        self.imu.enable()
        self.mag.enableLIS(magnetometer=True)

        self.imu.calibrateGyroAngles()

    def get_name(self):
        return self.name

    def get_channel(self):
        return self.channel

    def get_all(self, start):
        stop = datetime.now() - start
        deltaT = stop.microseconds/1000000.0

        
        # kalman = self.imu.getKalmanAngles(deltaT)
        comple = self.imu.getComplementaryAngles(deltaT)

        # print("Name:",self.name)
        # print("DeltaT:",deltaT)
        # print("Accel:", kalman)

        dataTuple = comple + [0,0,0]  + [0,0,0]

        return dataTuple
        # return [0, 0, 0, 0, 0, 0, 0, 0, 0]
