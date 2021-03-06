'''
NOTE: This code is deprecated. Similar processes are used in the updated code in file berryIMU.py
This code was based on Adafruit libraries 
(found somewhat better processing speed due to binary unpacking of registers rather than through Smbus reading register)
Unfortunately I'm not going to write the entire code to work with separate libraries so we'll go with the Ozzmaker ones.
'''



import board
import busio
import adafruit_lsm9ds1
import time
#import neopixel
from collections import deque
import RPi.GPIO as GPIO
import random
import json
from paho.mqtt import client as mqtt_client

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)

DEBUG = 1
MQTT = 1
PRINT = 1

windowSize = 20
pthreshold = 14
gthreshold = -150

broker = 'broker.emqx.io'
port = 1883
topic = "180d/team7"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

i2c = busio.I2C(board.SCL, board.SDA)
imu = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)
#p = neopixel.NeoPixel(board.D18, 8, auto_write=False, pixel_order=neopixel.GRBW)

_accX = deque()
_accY = deque()
_accZ = deque()
_gyX = deque()
_gyY = deque()
_gyZ = deque()


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
		p[4] = ((0,128
'''

def connect_mqtt():
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("Connected to MQTT Broker!")
		else:
			print("Failed to connect, return code %d\n", rc)

	client = mqtt_client.Client(client_id)
	client.on_connect = on_connect
	client.connect(broker, port)
	return client

def publish(client, action):
	global PRINT
	dict = {
		1: "b",
		2: "c",
		3: "h"
	}
	msg = json.dumps({"player": "player1", "action": dict[action]})
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f"Failed to send message to topic {topic}")

def setup():
	while len(_accX) < windowSize:
		ax,ay,az = imu.acceleration
		gx,gy,gz = imu.gyro
		_accX.append(ax)
		_accY.append(ay)
		_accZ.append(az)
		_gyX.append(gx)
		_gyY.append(gy)
		_gyZ.append(gz)

def loop():
	hitcounter = 0
	punchReg = False
	pubReg = False
	punchTime = time.time()
	client = connect_mqtt()

	global DEBUG
	global MQTT
	global PRINT

	iter = 0
	iterstart = punchTime
	while (1):
		client.loop_start()
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

		if PRINT:
			print(x, end='	\r', flush=True)

		if DEBUG:
			if avaX > pthreshold and avgX < gthreshold and punchReg == False: 
				print("Punch!", end='\n')
				punchReg = True
				pubReg = True
				hitcounter += 1
				GPIO.output(18,GPIO.HIGH)
				punchTime = time.time()
			if time.time() - punchTime >= 1:
				punchReg = False
				GPIO.output(18,GPIO.LOW)
#			if time.time() - iterstart >= 10:
#				print(iter)
		if MQTT:
			if pubReg:
				action = random.randint(1,3)
				publish(client, action)
				pubReg = False
		iter += 1

if __name__ == "__main__":
	setup()
	loop()
