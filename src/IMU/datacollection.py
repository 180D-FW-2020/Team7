import csv
import time
import sys
import IMU

DEBUG = 1

fname = "./data/{}.csv".format(time.strftime('%Y%m%d-%H%M%S'))

'''
    imu.accel_range = adafruit_lsm9ds1.ACCELRANGE_4G
    imu.gyro_scale = adafruit_lsm9ds1.GYROSCALE_2000DPS

    punchReg = False
    punchTime = time.time()
'''


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      
XL_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
GYRO_LPF_FACTOR = 0.4
#window = 40
_SENSORS_GRAVITY_STANDARD = 9.80665

oldXGyrRawValue = 0
oldYGyrRawValue = 0
oldZGyrRawValue = 0
oldXAccRawValue = 0
oldYAccRawValue = 0
oldZAccRawValue = 0

############ Helper functions to convert 16bit unsigned to readable data ############

def _accel(raw):
    return map(lambda x: x * _XL_MG_8G / 1000.0 * _SENSORS_GRAVITY_STANDARD, raw)

def _gyro(raw):
    return map(lambda x: x * _GYRO_DPS, raw)

############     won't deal with magnetometer. fuck the magnetometer.    ############

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

    while True:

        #Read the accelerometer,gyroscope and magnetometer values
        _ACCx = IMU.readACCx()
        _ACCy = IMU.readACCy()
        _ACCz = IMU.readACCz()
        _GYRx = IMU.readGYRx()
        _GYRy = IMU.readGYRy()
        _GYRz = IMU.readGYRz()

        ###############################################
        #### Apply low pass filter ####
        ###############################################
        GYRx =  _GYRx  * GYRO_LPF_FACTOR + oldXGyrRawValue*(1 - GYRO_LPF_FACTOR)
        GYRy =  _GYRy  * GYRO_LPF_FACTOR + oldYGyrRawValue*(1 - GYRO_LPF_FACTOR)
        GYRz =  _GYRz  * GYRO_LPF_FACTOR + oldZGyrRawValue*(1 - GYRO_LPF_FACTOR)
        ACCx =  _ACCx  * XL_LPF_FACTOR + oldXAccRawValue*(1 - XL_LPF_FACTOR)
        ACCy =  _ACCy  * XL_LPF_FACTOR + oldYAccRawValue*(1 - XL_LPF_FACTOR)
        ACCz =  _ACCz  * XL_LPF_FACTOR + oldZAccRawValue*(1 - XL_LPF_FACTOR)

        oldXGyrRawValue = GYRx
        oldYGyrRawValue = GYRy
        oldZGyrRawValue = GYRz
        oldXAccRawValue = ACCx
        oldYAccRawValue = ACCy
        oldZAccRawValue = ACCz

        ##################### END Ozzmaker code ########################

        buffer = [time.perf_counter() - a]
        #add raw vals to data
        buffer.extend(_accel((_ACCx,_ACCy,_ACCz)))
        buffer.extend(_gyro((_GYRx,_GYRy,_GYRz)))
        #add filtered vals to data
        buffer.extend(_accel((ACCx,ACCy,ACCz)))
        buffer.extend(_gyro((GYRx,GYRy,GYRz)))

        # will compare LPF to moving average
        # theoretically LPF has better cutoff & control
        # but moving average is hella easy (just require queue, 
        #       time complexity to add items is much better)


        if DEBUG:
            print(buffer, end='                 	\r', flush=True)
        csvwriter.writerow(buffer)
