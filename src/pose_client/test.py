#!/home/omar/.conda/envs/ece180da/bin/python3.
#####Necessary Includes
import json
import argparse
import logging
import time
import matplotlib.pyplot as plt
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import move_classification as fight

#Legacy example code for debugging, leaving because they might still need to be used
logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
#####Necesarry Constansts
fps_time = 0
debug = False
use_video = False
use_mqtt = False
w =432
h = 368
RESIZE_OUT_RATIO = 2.0


#Helpful functions for both doing parsing and the mqtt handling

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
def get_mqtt_header():
    return time.strftime("H%H-M%M-S%S", time.localtime()) + ":::"
def on_connect(client, userdata, flags, rc):
    print("Connection Returned result: " + str(rc))
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect")
    else:
        print("Expected Disconnect")
def on_message(client, userdata, message):
    #We should use this for start game and end game and all that, ####REMMEBER THIS LATER
    print("#######Received Message###########")
    print(str(message.payload))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--input', default='camera')
    parser.add_argument('--video', type=str, default='')
    parser.add_argument('--debug', default='false')
    parser.add_argument('--mqtt', type=str, default='')
    args = parser.parse_args()
    if(args.input.lower() == "video"):
        use_video = True
    if(args.debug.lower() == "true"):
        debug = True
    if(args.mqtt.lower() != ''):
        use_mqtt = True
        mqtt_channel = args.mqtt.lower()

    if use_mqtt:
        #Enabling MQTT, eclipise will be the constant server
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_message = on_message
        client.connect_async('broker.emqx.io')
        client.loop_start()
    logger.debug('initialization %s : %s' % ('mobilenet_thin', get_graph_path('mobilenet_thin')))
    e = TfPoseEstimator(get_graph_path('mobilenet_v2_small'), target_size=(w, h), trt_bool=str2bool("False"))
    #Allows us to either use video or camera as input(When finite video wil lnot exit cleanly)
    if use_video:
        cam = cv2.VideoCapture(args.video)
    else:
        cam = cv2.VideoCapture(0)
    if not (cam.isOpened()):
        print("Error opening video stream or file")
    ret_val, image = cam.read()


    while cam.isOpened():
        message = ""
        ret_val, image = cam.read()
        #humans is an object arr that contains all the ppl(0, 1, 1+ however many)
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=RESIZE_OUT_RATIO)
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
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
                        message = json.dumps({"player": "player1", "action": "o"})
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
                        (0, 255, 0), 2)

            cv2.imshow('tf-pose-estimation result VIDEO/WEBCAM', image)
        fps_time = time.time()

        if cv2.waitKey(1) == 27:
            break
        logger.debug('finished+')

    cv2.destroyAllWindows()
