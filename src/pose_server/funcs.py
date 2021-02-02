#!/usr/bin/python3
######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
import socket
import cv2
import numpy as np
import time
import pickle
import struct
from datetime import datetime
import sys
import os
from sys import platform
import argparse
import json
import argparse
import logging
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt
from funcs import *
sys.path.append('/usr/local/python');
from openpose import pyopenpose as op
from move_classification import *
LOAD_SIZE=691373
######MQTT functions##########
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
def get_mqtt_header():
    return time.strftime("H%H-M%M-S%S", time.localtime()) + ":::";
def on_connect(client, userdata, flags, rc):
    print("Connection Returned result: " + str(rc))
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect");
    else:
        print("Expected Disconnect");
def on_message(client, userdata, message):
    #We should use this for start game and end game and all that, ####REMMEBER THIS LATER
    print("#######Received Message###########");
    print(str(message.payload))

def create_mqtt_channel(mqtt_channel):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect_async('broker.emqx.io')
    client.loop_start()
    message = "BROADCAST TEST"
    client.publish(mqtt_channel, message, qos = 1)
    return client;
##########################Openpose functions#########################


def player_thread(client, opWrapper, mqtt_client, mqtt_channel, debug, addr):
    data = b''
    fps_time = 0;
    while True:
        payload_size = struct.calcsize("L")
        while len(data) < payload_size:
            #data += client.recv(90456)
            data += client.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        #print(str(msg_size))
        str_msg = str(msg_size);
        print("Size with last digit player" +str_msg);
        player_num = int(str_msg[-1]);
        msg_size = int(str_msg[:-1])
        player = "player" + str(player_num);
        print("Received input from " + player);
        while len(data) < msg_size:
            data += client.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        now = datetime.now()
        current_time = now.strftime("%M:%S")
        print (current_time + " -- "+ str(frame.size))
        datum = op.Datum()
        datum.cvInputData = frame#imageToProcess
        print ("\tpost process " + current_time + " -- "+ str(frame.size))
        stats = opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        print(str(stats));
        poseModel = op.PoseModel.BODY_25
        #print(op.getPoseBodyPartMapping(poseModel))
        #print("Body keypoints: \n" + str(datum.poseKeypoints))
        movement = move(datum.poseKeypoints);
        #####MQTT SEND IT#######
        if movement == "blocking":
            message = json.dumps({"player": player, "action": "o"})
        else:
            message = json.dumps({"player": player, "action": "x"})
        mqtt_client.publish(mqtt_channel, message, qos = 1)
        if debug:
            cv2.putText(datum.cvOutputData,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2);
            cv2.imshow(player, datum.cvOutputData)
            
        print("FPS: %f" % (1.0 / (time.time() - fps_time)));
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

        
