import board
import busio
import adafruit_lsm9ds1
import time
#import neopixel
from collections import deque
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

DEBUG = 1

i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
#p = neopixel.NeoPixel(board.D18, 8, auto_write=False, pixel_order=neopixel.GRBW)

_accX = deque()
_accY = deque()
_accZ = deque()
_gyX = deque()
_gyY = deque()
_gyZ = deque()

punchReg = False
punchTime = time.time()

'''
def movement(_ax,_ay,_az,_gx,_gy,_gz, _t):
	p.fill((0,0,0,0))
	if _ax < -1:
                p[0] = ((128,0,0,0))
	if _ax > 1:
		p[0] = ((0,128,0,0))
	if _ay < -1:
		p[1] = ((0,0,128,0))
	if _ay > 1:
		p[1] = ((66,128,0,0))
	if _az > 10.8:
		p[2] = ((0,44,128,0))
	if _az < 8.8:
		p[2] = ((128,128,0,0))
	if _gx > 90:
		p[5] = ((128,0,0,0))
	if _gx < -90:
		p[5] = ((0,128,0,0))
	if _gy > 90:
		p[6] = ((0,0,128,0))
	if _gy < -90:
		p[6] = ((66,128,0,0))
	if _gz > 90:
		p[7] = ((128,128,0,0))
	if _gz < -90:
		p[7] = ((0,44,128,0))
	if t <= 20:
		p[3] = ((0,0,128,10))
	if t >= 20:
		p[4] = ((0,128,0,10))
	p.show()
'''

while len(_accX) < 30:
	ax,ay,az = imu.acceleration
	gx,gy,gz = imu.gyro
	_accX.append(ax)
	_accY.append(ay)
	_accZ.append(az)
	_gyX.append(gx)
	_gyY.append(gy)
	_gyZ.append(gz)


while (1):
	ax,ay,az = imu.acceleration
	gx,gy,gz = imu.gyro
	t = imu.temperature
	_accX.popleft()
	_accY.popleft()
	_accZ.popleft()
	_gyX.popleft()
	_gyY.popleft()
	_gyZ.popleft()

	_accX.append(ax)
	_accY.append(ay)
	_accZ.append(az)
	_gyX.append(gx)
	_gyY.append(gy)
	_gyZ.append(gz)

	avaX = sum(_accX) / len(_accX)
	avaY = sum(_accY) / len(_accY)
	avaZ = sum(_accZ) / len(_accZ)
	avgX = sum(_gyX) / len(_gyX)
	avgY = sum(_gyY) / len(_gyY)
	avgZ = sum(_gyZ) / len(_gyZ)

	x = f"accel: ({avaX:.3f},{avaY:.3f},{avaZ:.3f}) gyro: ({avgX:.3f},{avgY:.3f},{avgZ:.3f}) temp: {t:.2f}"
#	movement(avaX,avaY,avaZ,avgX,avgY,avgZ, t)


	print(x, end='	\r', flush=True)

	if DEBUG:
		if avaX > 12 and punchReg == False: 
			print("Punch!", end='\n')
			punchReg = True
			GPIO.output(18,GPIO.HIGH)
			punchTime = time.time()
		if time.time() - punchTime >= 1:
			punchReg = False
			GPIO.output(18,GPIO.LOW)
		
