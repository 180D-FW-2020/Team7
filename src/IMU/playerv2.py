#!/usr/bin/python

from gesture_detector import gestureRecognizer
import argparse
import threading
import time
import random
import json
from paho.mqtt import client as mqtt_client

PRINT = 0
ID = 0

_XL_MG_8G = 0.2440       
_GYRO_DPS = 0.0700      

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
	client.connect_async(broker, port)
	return client

def publish(client, action, ID):
	global PRINT
	act = {
        "hook": "h",
        "cross": "c",
        "" : ""
        #"negative_trim": "lol"
    }
	msg = json.dumps({"playerID": ID, "action": act[action]})
	result = client.publish(topic, msg)
	# result: [0, 1]
	status = result[0]
	if status == 0:
		print(f"Send `{msg}` to topic `{topic}`")
	else:
		print(f"Failed to send message to topic {topic}")


if __name__ == "__main__":

#    global PRINT, ID

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

    hitcounter = 0
    punchReg = False
    pubReg = False
    punchTime = time.perf_counter()
    
    iter = 0

    client = connect_mqtt()

    imu = gestureRecognizer()
    pred = ""
    last_classification = ""

    sync = time.time()

    while 1:
        client.loop_start()

        #Read the accelerometer,gyroscope and magnetometer values
        gesture = [] + imu.collect()
        # look for a difference in pitch and yaw (about y- and z-axes of rotation)
        thresholdmeasure = (abs(gesture[0]) + abs(gesture[1]) + abs(gesture[2])) / 3

        if PRINT:
            print(gesture)


        if thresholdmeasure > 200:
            pred = imu.classify()
            punchReg = True
            print("lol")
        if time.perf_counter() - punchTime >= 1:
            punchReg = False


        if time.time() - sync > 5:
            publish(client, last_classification, ID)
            sync = time.time()
            last_classification = pred


            # if punchReg == False:

            #     if avaX > cXAcc and avgX > cGamma: # and avgZ > cAlpha: 
            #         print("Cross!", end='\n')
            #         punchReg = True
            #         pubReg = True
            #         hitcounter += 1
            #         action = "c"
            #         punchTime = time.perf_counter()

            #     if avaZ < hZAcc and avgZ > hAlpha and avgX < hGamma:
            #         print("Hook!", end='\n')
            #         punchReg = True
            #         pubReg = True
            #         hitcounter += 1
            #         action = "h"
            #         punchTime = time.perf_counter()

