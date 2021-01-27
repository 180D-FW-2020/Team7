#!/usr/bin/python3
import socket
import cv2
import pickle
import struct
from datetime import datetime
device = cv2.VideoCapture(-1)
ok, frame = device.read()

host = '72.134.122.226'
port = 5001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

while True:
    ok, frame = device.read()
    frame = cv2.resize(frame,(480,480));
    #frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)

    data = pickle.dumps(frame)
    client_socket.sendall(struct.pack("L", len(data)) + data)
    now = datetime.now()
    current_time = now.strftime("%M:%S")
    print(current_time);
    #cv2.imshow("",frame)
    #if cv2.waitKey(1) == 27:
    #    break

device.release()
cv2.destroyAllWindows()
