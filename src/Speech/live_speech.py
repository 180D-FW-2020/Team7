"""
Send only one message for mqtt per command recognized
Use for loop to sample audio every 5 seconds or so, 
then publish mqtt if command is detected
"""
import time
import random
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

def publish(client, action):
     while True:
         time.sleep(1)
         msg = f"Speech: {action}"
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
    publish(client, text)



import speech_recognition as sr
r=sr.Recognizer()

while(True):
	text = ""
	print("Please Talk!")
	with sr.Microphone() as source:
		canPublish = False
		audio_data=r.record(source, duration=5)
		print("Recognizing...")

		try:
			text=r.recognize_google(audio_data)
		except:
			print("waiting for next comand...")
		print("You said: ")
		print(text)
		
		# find if certain words exist within said phrase
		if(text.find("begin") != -1 or text.find("start") != -1):
			canPublish = True
			print("The game will start soon!")
		elif(text.find("fight") != -1):
			canPublish = True
			print("Fighting mode!")
		elif(text.find("stop") != -1 or text.find("pause") != -1):
			canPublish = True
			print("Game has stopped! Say 'Resume' or 'Restart' or 'Continue' to come back!")
			with sr.Microphone() as source2:
				audio_data2=r.record(source2, duration=5)
				print("Recognizing...")
				text2=r.recognize_google(audio_data2)
				print("You said: " + text2)
				if(text2.find("resume") != -1 or text2.find("restart") != -1 or text2.find("continue") != -1):
					print("Welcome back!")
		
		if(canPublish):
				if __name__ == '__main__':
					run()




