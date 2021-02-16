#!/usr/bin/python3.
import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    print("Connection Returned result: " + str(rc))
    client.subscribe("180d/team7", qos=1);
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnect");
    else:
        print("Expected Disconnect");
def on_message(client, userdata, message):
    #We should use this for start game and end game and all that, ####REMMEBER THIS LATER
    #this will print out weird..... we'll figure it out later
    print(str(message.payload))

client = mqtt.Client();
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

#client.connect_async('mqtt.eclipse.org');
client.connect_async('broker.emqx.io');

client.loop_start();
while True:
    pass
client.loop_stop();
client.disconnect();
