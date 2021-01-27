import csv
import time
import sys
import IMU
from collections import deque

DEBUG = 0

fname = "./data/{}.csv".format(time.strftime('%Y%m%d-%H%M%S'))

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      
# XL_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
# GYRO_LPF_FACTOR = 0.4
windowSize = 20
_SENSORS_GRAVITY_STANDARD = 9.80665

############ Helper functions to convert 16-bit unsigned to readable data ############

def _accel(raw):
    return map(lambda x: x * _XL_MG_8G / 1000.0 * _SENSORS_GRAVITY_STANDARD, raw)

def _gyro(raw):
    return map(lambda x: x * _GYRO_DPS, raw)

############     won't deal with magnetometer. fuck the magnetometer.     ############

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


with open(fname, 'w') as csvfile:


    header = ["time","aX","aY","aZ","gX","gY","gZ","faX","faY","faZ","fgX","fgY","fgZ"]

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    a = time.perf_counter()

    _accX = deque()
    _accY = deque()
    _accZ = deque()
    _gyrX = deque()
    _gyrY = deque()
    _gyrZ = deque()


    while len(_accX) < windowSize:
        ax,ay,az = _accel((IMU.readACCx(),IMU.readACCy(),IMU.readACCz()))
        gx,gy,gz = _gyro((IMU.readGYRx(),IMU.readGYRy(),IMU.readGYRz()))

        _accX.append(ax)
        _accY.append(ay)
        _accZ.append(az)
        _gyrX.append(gx)
        _gyrY.append(gy)
        _gyrZ.append(gz)


    while 1:

        #Read the accelerometer,gyroscope and magnetometer values
        _ACCx = IMU.readACCx()
        _ACCy = IMU.readACCy()
        _ACCz = IMU.readACCz()
        _GYRx = IMU.readGYRx()
        _GYRy = IMU.readGYRy()
        _GYRz = IMU.readGYRz()

        # ###############################################
        # #### Apply low pass filter ####
        # ###############################################
        # GYRx =  _GYRx  * GYRO_LPF_FACTOR + oldXGyrRawValue*(1 - GYRO_LPF_FACTOR)
        # GYRy =  _GYRy  * GYRO_LPF_FACTOR + oldYGyrRawValue*(1 - GYRO_LPF_FACTOR)
        # GYRz =  _GYRz  * GYRO_LPF_FACTOR + oldZGyrRawValue*(1 - GYRO_LPF_FACTOR)
        # ACCx =  _ACCx  * XL_LPF_FACTOR + oldXAccRawValue*(1 - XL_LPF_FACTOR)
        # ACCy =  _ACCy  * XL_LPF_FACTOR + oldYAccRawValue*(1 - XL_LPF_FACTOR)
        # ACCz =  _ACCz  * XL_LPF_FACTOR + oldZAccRawValue*(1 - XL_LPF_FACTOR)

        # oldXGyrRawValue = GYRx
        # oldYGyrRawValue = GYRy
        # oldZGyrRawValue = GYRz
        # oldXAccRawValue = ACCx
        # oldYAccRawValue = ACCy
        # oldZAccRawValue = ACCz

        # ##################### END Ozzmaker code ########################

        ax,ay,az = _accel((_ACCx,_ACCy,_ACCz))
        gx,gy,gz = _gyro((_GYRx,_GYRy,_GYRz))

        _accX.popleft()
        _accY.popleft()
        _accZ.popleft()
        _gyrX.popleft()
        _gyrY.popleft()
        _gyrZ.popleft()

        _accX.append(ax)
        _accY.append(ay)
        _accZ.append(az)
        _gyrX.append(gx)
        _gyrY.append(gy)
        _gyrZ.append(gz)


        avaX = sum(_accX) / len(_accX)
        avaY = sum(_accY) / len(_accY)
        avaZ = sum(_accZ) / len(_accZ)
        avgX = sum(_gyrX) / len(_gyrX)
        avgY = sum(_gyrY) / len(_gyrY)
        avgZ = sum(_gyrZ) / len(_gyrZ)


        buffer = [time.perf_counter() - a]
        #add raw vals to data
        buffer.extend((ax,ay,az))
        buffer.extend((gx,gy,gz))
        #add filtered vals to data
        buffer.extend((avaX,avaY,avaZ))
        buffer.extend((avgX,avgY,avgZ))


        if DEBUG:
            print(buffer, end='                 	\r', flush=True)
        csvwriter.writerow(buffer)
