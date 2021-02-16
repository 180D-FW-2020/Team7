#!/usr/bin/python3
import time


reg = False;

while True:
    cnt = time.time();
    if cnt % 5 == 0:
        reg = True;
        if reg:
            print(int(cnt % 60));
    if cnt % 5 == 1:
        reg = False
