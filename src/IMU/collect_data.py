import IMU
import time
import pandas as pd
import os
import sys
# import argparse
# from collections import deque


RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      
# windowSize = 10
_SENSORS_GRAVITY_STANDARD = 9.80665


def _accel(raw):
    return map(lambda x: x * _XL_MG_8G / 1000.0 * _SENSORS_GRAVITY_STANDARD, raw)

def _gyro(raw):
    return map(lambda x: x * _GYRO_DPS, raw)

def countdown(t):
    while t: 
        mins, secs = divmod(t, 60) 
        timer = f'{secs:02d}' 
        print(timer, end="  \r") 
        time.sleep(1) 
        t -= 1
    print( "go!")

IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

i = 0
header = ["time_ms", "delta_ms", "aX", "aY", "aZ", "gX", "gY", "gZ"]

filename = input("Name the folder where data will be stored: ")
if not os.path.exists(filename):
  os.mkdir(filename + '/')
starting_index = int(input("What number should we start on? "))

duration_s = float(input("Please input how long should a sensor trace be in seconds (floats OK): "))

i = starting_index
while True:
    
    c = input("Collecting file " + str(i)+ ". Press Q to exit, Enter to continue...")
    if c.lower() == 'q':
        sys.exit("Exited code.")

    data = []
    # _accX = deque(); _accY = deque(); _accZ = deque()
    # _gyrX = deque(); _gyrY = deque(); _gyrZ = deque()

    # while len(_accX) < windowSize: ## setup for filter
    #     ax,ay,az = _accel((IMU.readACCx(),IMU.readACCy(),IMU.readACCz()))
    #     gx,gy,gz = _gyro((IMU.readGYRx(),IMU.readGYRy(),IMU.readGYRz()))

    #     _accX.append(ax); _accY.append(ay); _accZ.append(az)
    #     _gyrX.append(gx); _gyrY.append(gy); _gyrZ.append(gz)

    countdown(3)

    start = time.perf_counter()
    elapsed_ms = 0
    previous_elapsed_ms = 0

    while elapsed_ms < duration_s * 1000:

        # data collection #
        
        _ACCx = IMU.readACCx(); _ACCy = IMU.readACCy(); _ACCz = IMU.readACCz()
        _GYRx = IMU.readGYRx(); _GYRy = IMU.readGYRy(); _GYRz = IMU.readGYRz()
        
        ###################


        # data processing #
        
        # ax,ay,az = _accel((_ACCx,_ACCy,_ACCz))
        # gx,gy,gz = _gyro((_GYRx,_GYRy,_GYRz))

        # _accX.popleft(); _accY.popleft(); _accZ.popleft()
        # _gyrX.popleft(); _gyrY.popleft(); _gyrZ.popleft()

        # _accX.append(ax); _accY.append(ay); _accZ.append(az)
        # _gyrX.append(gx); _gyrY.append(gy); _gyrZ.append(gz)

        # avaX = sum(_accX)/len(_accX); avaY = sum(_accY)/len(_accY); avaZ = sum(_accZ)/len(_accZ)
        # avgX = sum(_gyrX)/len(_gyrX); avgY = sum(_gyrY)/len(_gyrY); avgZ = sum(_gyrZ)/len(_gyrZ)

        ###################

        row = [elapsed_ms, int(elapsed_ms - previous_elapsed_ms)] 
        row.extend((_ACCx, _ACCy, _ACCz)); row.extend((_GYRx, _GYRy, _GYRz))
        # row.extend((avaX, avaY, avaZ)); row.extend((avgX, avgY, avgZ))

        data.append(row)
        previous_elapsed_ms = elapsed_ms
        elapsed_ms = (time.perf_counter() - start) * 1000

    if input("delete (n)? ").lower() == 'n':
        pass
    else:
        file_name = f"{filename}/{filename}{i:03d}.csv"
        df = pd.DataFrame(data, columns = header)
        df.to_csv(file_name, header=True)
        i += 1
    
