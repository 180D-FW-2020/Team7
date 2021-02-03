#!/usr/bin/python

import sys
import time
import math
import IMU
import argparse
from collections import deque

import random
import json
from paho.mqtt import client as mqtt_client

PLAY = 1
MQTT = 1
PRINT = 0
ID = 0

_accX = deque(); _accY = deque(); _accZ = deque()
_gyrX = deque(); _gyrY = deque(); _gyrZ = deque()



RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      
# XL_LPF_FACTOR = 0.4    # Low pass filter constant for accelerometer
# GYRO_LPF_FACTOR = 0.4
windowSize = 20
pThreshold = 14
gThreshold = 150
_SENSORS_GRAVITY_STANDARD = 9.80665


######### Thresholds #########



# cross-body punch
cXAcc = 13
#cAlpha = 160 # yaw
cGamma = 160 # roll

# hook (swing) punch
hZAcc = -14
hGamma = -90
hAlpha = 90
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

def publish(client, action, ID):
	global PRINT
	
	msg = json.dumps({"playerID": ID, "action": action})
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
    global PRINT, ID 


    parser = argparse.ArgumentParser(description = 'data collection stuff')
    parser.add_argument('--print', type = int, default = 0)
    parser.add_argument('--player', type = int, default = 0)

    args = parser.parse_args()
    if args.print == 1:
	    PRINT = 1
    if not (args.player == 1 or args.player == 2):
        print("Please input \"--player 1\" OR \"--player 2")
        exit()
    ID = args.player

    IMU.detectIMU()     #Detect if BerryIMU is connected.
    if(IMU.BerryIMUversion == 99):
        print(" No BerryIMU found... exiting ")
        sys.exit()
    IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


    while len(_accX) < windowSize:
        ax,ay,az = _accel((IMU.readACCx(),IMU.readACCy(),IMU.readACCz()))
        gx,gy,gz = _gyro((IMU.readGYRx(),IMU.readGYRy(),IMU.readGYRz()))

        _accX.append(ax); _accY.append(ay); _accZ.append(az)
        _gyrX.append(gx); _gyrY.append(gy); _gyrZ.append(gz)

def loop():
    global PLAY, MQTT, PRINT, ID
    
    hitcounter = 0
    punchReg = False
    pubReg = False
    punchTime = time.perf_counter()

    iter = 0

    client = connect_mqtt()

    while 1:

        client.loop_start()
        action = ""
        #Read the accelerometer,gyroscope and magnetometer values
        _ACCx = IMU.readACCx(); _ACCy = IMU.readACCy(); _ACCz = IMU.readACCz()
        _GYRx = IMU.readGYRx(); _GYRy = IMU.readGYRy(); _GYRz = IMU.readGYRz()

        ax,ay,az = _accel((_ACCx,_ACCy,_ACCz))
        gx,gy,gz = _gyro((_GYRx,_GYRy,_GYRz))

        _accX.popleft(); _accY.popleft(); _accZ.popleft()
        _gyrX.popleft(); _gyrY.popleft(); _gyrZ.popleft()

        _accX.append(ax); _accY.append(ay); _accZ.append(az)
        _gyrX.append(gx); _gyrY.append(gy); _gyrZ.append(gz)

        avaX = sum(_accX) / len(_accX); avaY = sum(_accY) / len(_accY); avaZ = sum(_accZ) / len(_accZ)
        avgX = sum(_gyrX) / len(_gyrX); avgY = sum(_gyrY) / len(_gyrY); avgZ = sum(_gyrZ) / len(_gyrZ)

        if PRINT:
            x = f"accel: ({avaX:.3f},{avaY:.3f},{avaZ:.3f}) gyro: ({avgX:.3f},{avgY:.3f},{avgZ:.3f})"
            print(x, end='	\r', flush=True)
        
        if PLAY:
            if punchReg == False:

                if avaX > cXAcc and avgX > cGamma: # and avgZ > cAlpha: 
                    print("Cross!", end='\n')
                    punchReg = True
                    pubReg = True
                    hitcounter += 1
                    action = "c"
                    punchTime = time.perf_counter()

                if avaZ < hZAcc and avgZ > hAlpha and avgX < hGamma:
                    print("Hook!", end='\n')
                    punchReg = True
                    pubReg = True
                    hitcounter += 1
                    action = "h"
                    punchTime = time.perf_counter()


            if time.perf_counter() - punchTime >= 1:
                punchReg = False

        if MQTT:
            if pubReg:
                publish(client, action, ID)
                pubReg = False

        iter += 1



if __name__ == "__main__":
    setup()
    loop()
