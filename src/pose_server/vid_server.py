#!/usr/bin/python3
######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
<<<<<<< HEAD
import threading
=======
<<<<<<< HEAD
import threading
=======
>>>>>>> d4d4049057f4be3683c33affad7317b130bfa763
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
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
<<<<<<< HEAD
from funcs import *
=======
<<<<<<< HEAD
from funcs import *
sys.path.append('/usr/local/python');
from openpose import pyopenpose as op
LOAD_SIZE=691373

######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
#####OpenPose inits, I'd rather see if something goes wrong with this
=======

>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
sys.path.append('/usr/local/python');
from openpose import pyopenpose as op
LOAD_SIZE=691373

######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
#####OpenPose inits, I'd rather see if something goes wrong with this
<<<<<<< HEAD
=======
debug = False
use_mqtt = False
>>>>>>> d4d4049057f4be3683c33affad7317b130bfa763
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
params = dict()
params["model_folder"] = "/home/omar/openpose/models/"
params["net_resolution"] = "240x240" #if you have a nice computer you can bump this number up
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
<<<<<<< HEAD
host = '192.168.1.4'  #NO ONE CHANGE THIS
port = 5001   #OR THIS
=======
<<<<<<< HEAD
host = '192.168.1.4'  #NO ONE CHANGE THIS
port = 5001   #OR THIS
client_socket = None
#binds to socket, ONLY Ken Suzuki's computer

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    server_socket.bind((host, port))


=======
host = '192.168.1.4'  #ken, you're allowed to change this, maybe
port = 5001
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
client_socket = None
#binds to socket, ONLY Ken Suzuki's computer

if __name__ == '__main__':
<<<<<<< HEAD
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    server_socket.bind((host, port))


=======
>>>>>>> d4d4049057f4be3683c33affad7317b130bfa763
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--debug', default='false');
    parser.add_argument('--mqtt', type=str, default='')
    args = parser.parse_args()
<<<<<<< HEAD
    debug = False;
=======
<<<<<<< HEAD
    debug = False;
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        mqtt_channel = args.mqtt.lower()
    else:
        print("NEED MQTT \"--mqtt *channel*\"");
        exit();
    client = create_mqtt_channel(mqtt_channel);
    server_socket.listen(5)    
    while True:
        conn, addr = server_socket.accept()
        conn.settimeout(5)#move this arround if you want, but 5 is good
        #player_thread(conn, opWrapper, client, mqtt_channel, debug);
        threading.Thread(target = player_thread,args = (conn, opWrapper, client, mqtt_channel, debug, addr)).start();
                         
        
=======
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        mqtt_channel = args.mqtt.lower()
    else:
        print("NEED MQTT \"--mqtt *channel*\"");
        exit();
    client = create_mqtt_channel(mqtt_channel);
    server_socket.listen(5)    
    while True:
<<<<<<< HEAD
        conn, addr = server_socket.accept()
        conn.settimeout(5)#move this arround if you want, but 5 is good
        #player_thread(conn, opWrapper, client, mqtt_channel, debug);
        threading.Thread(target = player_thread,args = (conn, opWrapper, client, mqtt_channel, debug, addr)).start();
                         
        
=======
        while len(data) < payload_size:
            #data += conn.recv(90456)
            data += conn.recv(4096)

        packed_msg_size = data[:payload_size]

        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]
        #print(str(msg_size))
        str_msg = str(msg_size);
        player_num = int(str_msg[-1]);
        msg_size = int(str_msg[:-1])
        player = "player" + str(player_num);
        print("Received input from " + player);
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        now = datetime.now()
        current_time = now.strftime("%M:%S")
    
        print (current_time + " -- "+ str(frame.size))
    
        # Process Image
        #imageToProcess = cv2.imread(frame)
        datum = op.Datum()
        datum.cvInputData = frame#imageToProcess
        print ("\tpost process " + current_time + " -- "+ str(frame.size))
        #cv2.imshow('frame', frame)
        #cv2.waitKey(1)
        opWrapper.emplaceAndPop(op.VectorDatum([datum]))
        print("Body keypoints: \n" + str(datum.poseKeypoints))
        #####MQTT SEND IT#######
        message = json.dumps({"player": player, "action": "o"})
        client.publish(mqtt_channel, message, qos = 1)
        if debug:
            #cv2.putText(datum.cvOutputData,
            #"FPS: %f" % (1.0 / (time.time() - fps_time)),
            #(10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #(0, 255, 0), 2);
            
            cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM',datum.cvOutputData)
            #cv2.imshow("OpenPose 1.7.0 - Tutorial Python API", datum.cvOutputData)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

>>>>>>> d4d4049057f4be3683c33affad7317b130bfa763
>>>>>>> 9f4658fdfbfa65f886b248363ae87b6e10f654ce
