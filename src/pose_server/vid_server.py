#!/usr/bin/python3
######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
import threading
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
LOAD_SIZE=691373

######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
#####OpenPose inits, I'd rather see if something goes wrong with this
params = dict()
params["model_folder"] = "/home/omar/openpose/models/"
params["net_resolution"] = "240x240" #if you have a nice computer you can bump this number up
params["number_people_max"] = "1"
opWrapper = op.WrapperPython()
opWrapper.configure(params)
opWrapper.start()
host = '192.168.1.4'  #NO ONE CHANGE THIS
port = 5001   #OR THIS
client_socket = None
#binds to socket, ONLY Ken Suzuki's computer

if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--debug', default='false');
    parser.add_argument('--mqtt', type=str, default='')
    parser.add_argument('--host', type=str, default='');
    parser.add_argument('--port', type=int, default=-1);
    args = parser.parse_args()
    ##if other port is needed
    if(args.port != -1):
        print("Changing host port to " + str(args.port))
        port = args.port;
    ##If other cpu needs to be specified
    if(args.host.lower() != ""):
        print("Changeing Host addr to " + args.host.lower());
        host = args.host.lower();
    debug = False;
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        mqtt_channel = args.mqtt.lower()
    else:
        print("NEED MQTT \"--mqtt *channel*\"");
        exit();
    server_socket.bind((host, port))
    client = create_mqtt_channel(mqtt_channel);
    server_socket.listen(5)    
    while True:
        conn, addr = server_socket.accept()
        conn.settimeout(5)#move this arround if you want, but 5 is good
        #player_thread(conn, opWrapper, client, mqtt_channel, debug);
        threading.Thread(target = player_thread,args = (conn, opWrapper, client, mqtt_channel, debug, addr)).start();
                         
        
