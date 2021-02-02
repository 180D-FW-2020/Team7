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
import time
import signal

fps_time = 0
debug = False
use_video = False
w =432
h = 368
RESIZE_OUT_RATIO = 2.0
host = '72.134.122.226'#THIS IS CONSTANT
port = 5001 #SO IS THIS

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
 #THIS IS CONSTANT


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
signal_catch = False;



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='realtime broadcasting webcam')
    parser.add_argument('--input', default='camera')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--debug', default='false');
    parser.add_argument('--player', type=int, default=-1);

    args = parser.parse_args()

    if(args.input.lower() == "video"):
        use_video = True
    if(args.debug.lower() == "true"):
        debug = True
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





    while True:
        frame_num += 1;
        print(frame_num)
        if frame_num % 35 == 0:

            ok, frame = device.read()
            try:
                frame = cv2.resize(frame,(480,480));
            except:
                break;
            #frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
            data = pickle.dumps(frame)

            synth = str(len(data)) + str(args.player);
            print(str(len(data)))
            print(synth)

            int_synth = int(synth)
            print(int_synth)
            #client_socket.sendall(struct.pack("L", len(data), args.player) + data)
            client_socket.sendall(struct.pack("L", int_synth) + data)
            #print(str(len(struct.pack("L", int_synth) + data)))
            now = datetime.now()
            current_time = now.strftime("%M:%S")
            print(current_time);
            print("Current frame:" + str(frame_num));
            object = cv2();
            if(signal_catch == True):
                exit(0);
            if debug:
                object.putText(frame,
                            "FPS: %f" % (1.0 / (time.time() - fps_time)),
                            (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2);
                cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM', frame)
                if cv2.waitKey(1) == 27:
                    break
            fps_time = time.time()
            #client_socket.close();
    device.release()
    client_socket.close()
    cv2.destroyAllWindows()
