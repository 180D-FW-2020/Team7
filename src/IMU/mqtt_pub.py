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
         '''
         "b" for boxing
         "h" for hook
         "c" for cross
         "u" for receive uppercut
         "t" for take punch
         "s" for receive stomach uppercut
         all else ignored
         '''
         action = input("press key: ")
         msg = {"player" : "player1", "action" : action}
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
