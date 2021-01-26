"""
Send only one message for mqtt per command recognized
Use for loop to sample audio every 5 seconds or so, 
then publish mqtt if command is detected
"""
import time
import random
import json
from paho.mqtt import client as mqtt_client
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
         msg = {"player" : "player1", "action" : action}
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
		if(text.find("begin") != -1 or text.find("start") != -1):
			canPublish = True
			action = 'g'
			print("The game will start!")
		elif(text.find("resume") != -1 or text.find("pause") != -1):
			canPublish = True
			action = 'p'
			print("Paused/Resumed")
		elif(text.find("quit") != -1):
			canPublish = True
			action = 'q'
			print("Game quitted")
		
		if(canPublish):
				if __name__ == '__main__':
					run()
