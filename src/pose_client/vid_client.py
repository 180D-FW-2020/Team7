#!/usr/bin/python3
import socket
import cv2
import pickle
import struct
from datetime import datetime
import json
import argparse
import logging
import time
import matplotlib.pyplot as plt
import numpy as np
import paho.mqtt.client as mqtt
import time


fps_time = 0
debug = False
use_video = False
use_mqtt = False
w =480
h = 480
RESIZE_OUT_RATIO = 2.0
host = '72.134.122.226'#THIS IS CONSTANT
port = 5001 #SO IS THIS


 #THIS IS CONSTANT


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='realtime broadcasting webcam')
    parser.add_argument('--input', default='camera')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--debug', default='false');
    parser.add_argument('--mqtt', type=str, default='')
    parser.add_argument('--player', type=int, default=-1);
    args = parser.parse_args()
    if(args.input.lower() == "video"):
        use_video = True
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        mqtt_channel = args.mqtt.lower()
    if not (args.player == 1 or args.player == 2):
        print("Please input \"--player 1\" OR \"--player 2");
        exit();

    if use_video:
        device = cv2.VideoCapture(args.video)
    else:
        device = cv2.VideoCapture(0)
    if not (device.isOpened()):
        print("Error opening video stream or file")
        exit();
    frame_num = 0;

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))


    while True:
        ok, frame = device.read()
        frame = cv2.resize(frame,(480,480));
        #frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)

        data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("L", len(data)) + data)
        now = datetime.now()
        current_time = now.strftime("%M:%S")
        print(current_time);
        print("Current frame:" + str(frame_num)); frame_num += 1;
        if debug:
            cv2.putText(frame,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2);

            cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM', frame)
            if cv2.waitKey(1) == 27:
                break
        fps_time = time.time()

device.release()
cv2.destroyAllWindows()
