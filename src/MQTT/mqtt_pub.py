import time
import random
import json
from paho.mqtt import client as mqtt_client
broker = 'broker.emqx.io'
port = 1883
topic = "180d/team7"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

playerID = 1

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
         only boxers:
             "b" - Boxing
             "h" - Hook Punch
             "c" - Cross Punch
             "o" - Body Block
         only player 3:
             "p" - pause/resume game (in boxing scene)
             "q" - quit (in boxing scene)
             "g" - start game (in menu scene)
             arbitrary string from speech (in boxing scene)
             "r" - restart (after knocked out)
         all else ignored
         '''
         action = input("enter command: ")
         msg = {"playerID" : playerID, "action" : action}
         msg = json.dumps(msg)
         result = client.publish(topic, msg)
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send `{msg}` to topic `{topic}`")

         else:
             print(f"Failed to send message to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client, "test action")


if __name__ == '__main__':
    run()