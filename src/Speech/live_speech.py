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
import speech_recognition as sr

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

def countdown(t):
    while t: 
        secs = divmod(t, 60)[1] 
        timer = f'{secs:02d}' 
        print(f"Mic is blocked for {timer} seconds", end="  \r") 
        time.sleep(1) 
        t -= 1
    print( "\nMic is open!")




if __name__ == "__main__":
    unity = False;
    # contains trains of r/p, used to keep track of current status of either resumed or paused
    previousIs = "r"
    parser = argparse.ArgumentParser(description='realtime broadcasting webcam')
    parser.add_argument('--unity', default='false')
    args = parser.parse_args()
    if(args.unity.lower() == "true"):
        unity = True;
        if unity:
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


        if platform=="linux":
            print("Opening boxing.exe")
            subprocess.run(process_call + " &", shell=True)
        if platform=="win32":
            subprocess.Popen([process_call, str(args.player)])
    r=sr.Recognizer()
    # if platform=="linux":
    #     subprocess.run(process_call + " &", shell=True)
    # if platform=="win32":
    #     subprocess.Popen([process_call])


    countdown(10)
    while(True):

        text = ""
        action = ''

        if input("Press M to open mic for 3 seconds: ").lower() == "m":
            with sr.Microphone() as source:
                spoken = True
                canPublish = False
                print("Speak!")
                audio_data=r.record(source, duration=3)
                
                try:
                    text=r.recognize_google(audio_data)
                except:
                    spoken = False
                    print("Waiting for next command...")

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
                        print("Game quit")
                    else:
                        canPublish = True
                        action = text
                        print(f"Sending comments: {text}")

                    if(canPublish):
                        run()
