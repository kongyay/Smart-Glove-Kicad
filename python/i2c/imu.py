#!/usr/bin/python

from datetime import datetime
from time import sleep
from altimu import AltIMU
from lis3mdl import LIS3MDL
from math import sin,cos,atan2

class IMU(object):
    def __init__(self, channel=0, name=None):
        self.channel = channel
        self.name = name if name != None else channel
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
        stop = datetime.now() 
        deltaT = (stop-start).microseconds/1000000.0
        new_start = stop

        try:
            # [roll,pitch,yaw] = self.imu.getKalmanAngles(deltaT)
            # [roll,pitch,yaw] = self.imu.getAccelerometerAngles()
            # [roll,pitch,yaw] = self.imu.getComplementaryAngles(deltaT,self.name)
            # [magX,magY,magZ] = self.mag.getMagnetometerRaw()
            dataTuple = self.imu.getAccelerometerRaw() + self.imu.getGyroRotationRates()  
            # dataTuple = [roll,pitch,yaw]
            # print("Name:",self.name)
            # print("DeltaT:",deltaT)
            # print("Accel:", kalman)
        except (Exception):
            try:
                self.enable()
            except (Exception):
                print("Re-enable fail #", self.get_channel())
            
            dataTuple = [0,0,0]
        

        return dataTuple, new_start
        # return [0, 0, 0, 0, 0, 0, 0, 0, 0]
