import csv
import time
import board
import busio
import adafruit_lsm9ds1
import RPi.GPIO as GPIO

from collections import deque

DEBUG = 0
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

fname = "./data/{}.csv".format(time.strftime('%Y%m%d-%H%M%S'))

with open(fname, 'w') as csvfile:
    i2c = busio.I2C(board.SCL, board.SDA)
    imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

    imu.accel_range = adafruit_lsm9ds1.ACCELRANGE_4G
    imu.gyro_scale = adafruit_lsm9ds1.GYROSCALE_2000DPS

    punchReg = False
    punchTime = time.time()

    windowSize = 20
    pthreshold = 14
    gthreshold = -150

    header = ["time","aX","aY","aZ","gX","gY","gZ","faX","faY","faZ","fgX","fgY","fgZ","temp","punchReg","punchCount",f"{windowSize}",f"{pthreshold}",f"{gthreshold}"]

    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    t = time.time()

    _accX = deque()
    _accY = deque()
    _accZ = deque()
    _gyX = deque()
    _gyY = deque()
    _gyZ = deque()
#    _magX = deque()
#    _magY = deque()
#    _magZ = deque()

    while len(_accX) < windowSize:
        ax,ay,az = imu.acceleration
        gx,gy,gz = imu.gyro
#        mx,my,mz = imu.magnetic
        _accX.append(ax)
        _accY.append(ay)
        _accZ.append(az)
        _gyX.append(gx)
        _gyY.append(gy)
        _gyZ.append(gz)
#        _magX.append(mx)
#        _magY.append(my)
#        _magZ.append(mz)

    punchCounter = 0
    while 1:
        ax,ay,az = imu.acceleration
        gx,gy,gz = imu.gyro
#        mx,my,mz = imu.magnetic
        temp = imu.temperature

        _accX.popleft()
        _accY.popleft()
        _accZ.popleft()
        _gyX.popleft()
        _gyY.popleft()
        _gyZ.popleft()
#        _magX.popleft()
#        _magY.popleft()
#        _magZ.popleft()

        _accX.append(ax)
        _accY.append(ay)
        _accZ.append(az)
        _gyX.append(gx)
        _gyY.append(gy)
        _gyZ.append(gz)
#        _magX.append(mx)
#        _magY.append(my)
#        _magZ.appendleft(mz)

        avaX = sum(_accX) / len(_accX)
        avaY = sum(_accY) / len(_accY)
        avaZ = sum(_accZ) / len(_accZ)
        avgX = sum(_gyX) / len(_gyX)
        avgY = sum(_gyY) / len(_gyY)
        avgZ = sum(_gyZ) / len(_gyZ)
#        avmX = sum(_magX) / len(_magX)
#        avmY = sum(_magY) / len(_magY)
#        avmZ = sum(_magZ) / len(_magZ)

        if avaX > pthreshold and avgX < gthreshold and punchReg == False: 
            punchReg = True
            punchCounter += 1
            print(f"Punch! {punchCounter}", end='\n')
            GPIO.output(18,GPIO.HIGH)
            punchTime = time.time()
        if time.time() - punchTime >= 1:
            punchReg = False
            GPIO.output(18,GPIO.LOW)

        buffer = [time.time() - t]
        buffer.extend(imu.acceleration)
        buffer.extend(imu.gyro)
#        buffer.extend(imu.magnetic)
        buffer.extend((avaX, avaY, avaZ))
        buffer.extend((avgX, avgY, avgZ))
#        buffer.extend((avmX, avmY, avmZ))
        buffer.append(temp)
        buffer.append(punchReg)
        buffer.append(punchCounter)

        if DEBUG:
            print(buffer, end='	\r', flush=True)
        csvwriter.writerow(buffer)
