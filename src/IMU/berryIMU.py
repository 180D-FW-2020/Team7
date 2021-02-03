#!/usr/bin/python

import sys
import time
import math
import IMU

import random
import json
from paho.mqtt import client as mqtt_client

DEBUG = 1
MQTT = 1
PRINT = 1

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      
# XL_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
# GYRO_LPF_FACTOR = 0.4
windowSize = 20
pThreshold = 14
gThreshold = -150
_SENSORS_GRAVITY_STANDARD = 9.80665

############ MQTT ############

broker = 'broker.emqx.io'
port = 1883
topic = "180d/team7"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

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
	msg = json.dumps({"player": 1, "action": dict[action]})
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f"Failed to send message to topic {topic}")


############ Helper functions to convert 16-bit unsigned to readable data ############

def _accel(raw):
    return map(lambda x: x * _XL_MG_8G / 1000.0 * _SENSORS_GRAVITY_STANDARD, raw)

def _gyro(raw):
    return map(lambda x: x * _GYRO_DPS, raw)

############     won't deal with magnetometer. fuck the magnetometer.     ############

def setup():
    IMU.detectIMU()     #Detect if BerryIMU is connected.
    if(IMU.BerryIMUversion == 99):
        print(" No BerryIMU found... exiting ")
        sys.exit()
    IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


    while len(_accX) < windowSize:
        ax,ay,az = _accel((IMU.readACCx(),IMU.readACCy(),IMU.readACCz()))
        gx,gy,gz = _gyro((IMU.readGYRx(),IMU.readGYRy(),IMU.readGYRz()))

        _accX.append(ax)
        _accY.append(ay)
        _accZ.append(az)
        _gyrX.append(gx)
        _gyrY.append(gy)
        _gyrZ.append(gz)

def loop():
    global DEBUG, MQTT, PRINT
    
    hitcounter = 0
    punchReg = False
    pubReg = False
    punchTime = time.perf_counter()

    iter = 0
    iterStart = punchTime

    client = connect_mqtt()

    while 1:

        client.loop_start()

        #Read the accelerometer,gyroscope and magnetometer values
        _ACCx = IMU.readACCx(); _ACCy = IMU.readACCy(); _ACCz = IMU.readACCz()
        _GYRx = IMU.readGYRx(); _GYRy = IMU.readGYRy(); _GYRz = IMU.readGYRz()

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

        if PRINT:
            x = f"accel: ({avaX:.3f},{avaY:.3f},{avaZ:.3f}) gyro: ({avgX:.3f},{avgY:.3f},{avgZ:.3f}) temp: {t:.2f}"
			print(x, end='	\r', flush=True)
        
        if DEBUG:
            if avaX > pthreshold and avgX < gthreshold and punchReg == False: 
                print("Punch!", end='\n')
                punchReg = True
                pubReg = True
                hitcounter += 1
                GPIO.output(18,GPIO.HIGH)
                punchTime = time.perf_counter()

            if time.perf_counter() - punchTime >= 1:
                punchReg = False
                GPIO.output(18,GPIO.LOW)

        if MQTT:
            if pubReg:
                action = random.randint(1,3)
                publish(client, action)
                pubReg = False

        iter += 1