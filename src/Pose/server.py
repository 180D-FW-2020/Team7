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
import tensorflow as tf
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import move_classification as fight

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
#sys.path.append('/usr/local/python');
#from openpose import pyopenpose as op
#import pyopenpose as op
LOAD_SIZE=691373
RESIZE_OUT_RATIO = 2.0
w = 432
h = 368
fps_time = 0

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
######################DOOOO NOTTTTTT TOUUCHHHHHHHH #########################
#####OpenPose inits, I'd rather see if something goes wrong with this
debug = False
use_mqtt = False
params = dict()
params["model_folder"] = "/home/omar/openpose/models/"
params["net_resolution"] = "240x240" #if you have a nice computer you can bump this number up
host = '192.168.1.4'  #ken, you're allowed to change this, maybe
port = 5001
client_socket = None
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))


############################ POSE init #############################
# opWrapper = op.WrapperPython()
# opWrapper.configure(params)
# opWrapper.start()
e = TfPoseEstimator(get_graph_path('cmu'), target_size=(w, h), trt_bool=str2bool("False"), tf_config=tf.ConfigProto(log_device_placement=True))
#################################Wait for Connection###########################
#binds to socket, ONLY Ken Suzuki's computer
server_socket.listen(5)
conn, addr = server_socket.accept()


data = b''
payload_size = struct.calcsize("L")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--debug', default='false');
    parser.add_argument('--mqtt', type=str, default='')
    args = parser.parse_args()
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        use_mqtt = True
        mqtt_channel = args.mqtt.lower()
    else:
        print("NEED MQTT \"--mqtt *channel*\"");

    if use_mqtt:
        #Enabling MQTT, eclipise will be the constant server
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.connect_async('broker.emqx.io')
        client.loop_start()
        message = "BROADCAST TEST"
        client.publish(mqtt_channel, message, qos = 1)


    while True:

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
        humans = e.inference(frame, resize_to_default=(w > 0 and h > 0), upsample_size=RESIZE_OUT_RATIO)
        image = TfPoseEstimator.draw_humans(frame, humans, imgcopy=False)
        #fight.print_humans_info(humans)
        #Need to get human number later, and be able to parse through them, butt now we only need one
        humans_num = fight.parse_humans(humans)
        #Need to guarantee theres humans so that there exists memory to access
        if humans_num:
            #Part count of 14 makes sure theres some clean things
            if humans[0].part_count() > 11:
                #try-catch block here is garbage code, but is nice for demo
                #YOU MUST FIX BEFORE WINTER
                try:
                    # fight.are_knees_square(humans[0])
                    # fight.are_shoulders_square(humans[0])
                    # fight.is_right_arm_straight_down(humans[0])
                    # fight.is_left_arm_straight_down(humans[0])
                    fight.print_arms_blocking_head(humans[0])
                    #obviouslt here will be more precise looking on later, but for now, checking for one block
                    if fight.are_arms_blocking_head(humans[0]):
                        message = json.dumps({"player": player, "action": "o"})
                    else:
                        pass
                    #Golden child, lets publish this ish to the internet
                    if use_mqtt and message != "":
                        client.publish(mqtt_channel, message, qos = 1)
                        print("######Sending Message##########\n" + message)
                except:
                    print("Error with parsing")
        #cv2.putText(image,"FPS: %f" % (1.0 / (time.time() - fps_time)),(10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 2)
        #prints out video to screen so we can debut visually and see
        if debug:
            cv2.putText(image,
                        "FPS: %f" % (1.0 / (time.time() - fps_time)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2);

            cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM', image)
        print("FPS: %f" % (1.0 / (time.time() - fps_time)))
        #sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
        #print(sess);
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        logger.debug('finished+')
    cv2.destroyAllWindows()
    server_socket.close()