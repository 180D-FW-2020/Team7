#!/usr/bin/python3
import os
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
import subprocess
import zipfile
from sys import platform

if not os.path.isfile("../old/Boxing.exe"):
    if platform == "linux":
        if not os.path.isfile(os.path.abspath("../old/Boxing_v5.zip")):
            print("boxing_v5.zip does not exist, exiting")
            exit(-1)
        subprocess.call("unzip ../old/Boxing_v5.zip -d ../old", shell=True)
    if platform == "win32":
        with zipfile.ZipFile("../old/Boxing_v5.zip","r") as zip_ref:
            zip_ref.extractall("../old/")
    if not os.path.isfile("../old/Boxing.exe"):
        print("Boxing.exe does not exist")
        exit(-1)
if platform == "linux": subprocess.call("chmod +x ../old/Boxing.exe", shell=True)


if platform == "linux":
    process_call = "wine ../old/Boxing.exe 3"
elif platform == "win32":
    process_call = "../old/Boxing.exe"


fps_time = 0
debug = False
use_video = False
w =480
h = 480
RESIZE_OUT_RATIO = 2.0
host = '72.134.122.226'# THIS IS CONSTANT
port = 5001 #SO IS THIS
 #THIS IS CONSTANT
def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
signal_catch = False 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='realtime broadcasting webcam')
    parser.add_argument('--input', default='camera')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--debug', default='false') 
    parser.add_argument('--player', type=int, default=-1) 
    parser.add_argument('--host', type=str, default='') 
    parser.add_argument('--port', type=int, default=-1) 
    args = parser.parse_args()
    if(args.port != -1):
        print("Changing host port to " + str(args.port))
        port = args.port 
    if(args.host.lower() != ""):
        print("Changeing Host addr to " + args.host.lower()) 
        host = args.host.lower() 
    if(args.input.lower() == "video"):
        use_video = True
    if(args.debug.lower() == "true"):
        debug = True
    if not (args.player == 1 or args.player == 2):
        print("Please input \"--player 1\" OR \"--player 2") 
        exit() 

    if use_video:
        device = cv2.VideoCapture(args.video)
    else:
        device = cv2.VideoCapture(0)
    if not (device.isOpened()):
        print("Error opening video stream or file")
        exit()
    frame_num = 0 
    #process_call = process_call + " " + str(args.player)  #add player to argument
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except:
        print("Host " + str(host) + " is not accepting connections") 
        print("Please make sure server is accepting connections") 
        exit() 



    if platform=="linux":
        print("Opening boxing.exe")
        subprocess.run(process_call + " &", shell=True)
    if platform=="win32":
        subprocess.Popen([process_call, str(args.player)])


    while True:
        frame_num += 1
        #print(frame_num)
        if frame_num % 5 == 0:
            ok, frame = device.read()
#            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame,(480,480))
            #frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
            data = pickle.dumps(frame)

            synth = str(len(data)) + str(args.player)
            #print(str(len(data)))
            #print(synth)

            int_synth = int(synth)
            #print(int_synth)
            #client_socket.sendall(struct.pack("L", len(data), args.player) + data)

            client_socket.sendall(struct.pack("L", int_synth) + data)
            #print(str(len(struct.pack("L", int_synth) + data)))
            now = datetime.now()
            current_time = now.strftime("%M:%S")
            print("\nSent vid stream frame to " + str(host))
            print("\tCurrent Time " + str(current_time))
            print("\tCurrent frame:" + str(frame_num)) 
            print("\tFrames being sent at FPS: %f" % (1.0 / (time.time() - fps_time)))

            if(signal_catch == True):
                exit(0) 
            if debug:
                cv2.putText(frame,
                            "FPS: %f" % (1.0 / (time.time() - fps_time)),
                            (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 255, 0), 2) 

                cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM', frame)
                if cv2.waitKey(1) == 27:
                    break
            fps_time = time.time()

    device.release()
    cv2.destroyAllWindows()
