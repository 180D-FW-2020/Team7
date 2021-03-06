"""
Send only one message for mqtt per command recognized
Use for loop to sample audio every 5 seconds or so,
then publish mqtt if command is detected
"""
import time
import random
import json
from paho.mqtt import client as mqtt_client
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
            print("boxing_v5.zip does not exist, exiting");
            exit(-1);
        subprocess.call("unzip ../old/Boxing_v5.zip -d ../old", shell=True);
    if platform == "win32":
        with zipfile.ZipFile("../old/Boxing.exe","r") as zip_ref:
            zip_ref.extractall("../old/")
    if not os.path.isfile("../old/Boxing.exe"):
        print("Boxing.exe does not exist");
        exit(-1);
if platform == "linux": subprocess.call("chmod +x ../old/Boxing.exe", shell=True);


if platform == "linux":
    process_call = "wine ../old/Boxing.exe 3"
elif platform == "win32":
    process_call = "../old/Boxing.exe 3"

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
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

action = ''
def publish(client, action):
     while True:
         time.sleep(1)
         '''
         "b" - Boxing
         "h" - Hook Punch
         "c" - Cross Punch
         "o" - Body Block
         "u" - Receive Uppercut
         "t" - Taking Punch
         "s" - Receive Stomach Uppercut
         "p" - pause/resume game (in boxing scene)
         "g" - start game (in menu scene)
         all else ignored
         '''
         #action = input("press key: ")
         msg = {"playerID" : 3, "action" : action}
         msg = json.dumps(msg)
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")
         break

def run():
    client = connect_mqtt()
    #client.loop_start()
    publish(client, action)

import speech_recognition as sr
r=sr.Recognizer()

# contains trains of r/p, used to keep track of current status of either resumed or paused
previousIs = "r"

if platform=="linux":
    subprocess.call(process_call + " &", shell=True);
if platform=="win32":
    subprocess.call([process_call]);

while(True):
    text = ""
    action = ''
    print("Please Talk!")
    with sr.Microphone() as source:
        spoken = True
        canPublish = False
        audio_data=r.record(source, duration=3)
        print("Recognizing...")
        try:
            text=r.recognize_google(audio_data)
        except:
            spoken = False
            print("waiting for next comand...")

        if(spoken):
            print("You said: {}".format(text))
            # find if certain words exist within said phrase
            if(text.find("restart") != -1):
                canPublish = True
                action = 'r'
                print("Restarting")
            elif(text.find("begin") != -1 or text.find("start") != -1):
                canPublish = True
                action = 'g'
                print("The game will start!")
            elif(text.find("pause") != -1):
                if(previousIs[len(previousIs) - 1] == 'r'):
                    canPublish = True
                    action = 'p'
                    previousIs += 'p'
                    print("Paused")
            elif(text.find("resume") != -1):
                if(previousIs[len(previousIs) - 1] == 'p'):
                    canPublish = True
                    action = 'p'
                    previousIs += 'r'
                    print("Resumed")
            elif(text.find("quit") != -1):
                canPublish = True
                action = 'q'
                print("Game quitted")
            else:
                canPublish = True
                action = text
                print("Sending comments")

            if(canPublish):
                if __name__ == '__main__':
                    run()
