import argparse
import logging
import time
import matplotlib.pyplot as plt
import cv2
import numpy as np
import slidingwindow as sw
import tensorflow as tf
import time


#preset constants, DO NOT CHANGE
Nose = 0
Neck = 1
RShoulder = 2
RElbow = 3
RWrist = 4
LShoulder = 5
LElbow = 6
LWrist = 7
Waist = 8
RHip = 9
RKnee = 10
RAnkle = 11
LHip = 12
LKnee = 13
LAnkle = 14
REye = 15
LEye = 16
REar = 17
LEar = 18


##############################Coordinate Debugging###############
class body_part:
    def __init__(self, x, y):
        self.x = x; self.y = y
class person:
    def __init__(self, humans_num):
        self.body_parts = []
        for i in humans_num:
            x = i[0]
            y = i[1]
            #print("coordinates X: " + str(i[0]) + " Y:" + str(i[0]));
            tmp_body_part = body_part(x,y)
            self.body_parts.append(tmp_body_part)
        #print("Size of human ppl " + str(len(body_parts)));



def move(human_arr):

    # human_count = len(human_arr);
    # #print("human number is " + str(human_count));
    # human_nums = human_arr[0];
    # #print(human_nums);
    # human = person(human_nums);
    # print_arms_blocking_head(human);


    try:

        human_count = len(human_arr)
        #print("human number is " + str(human_count))
        human_nums = human_arr[0]
        #print(human_nums)
        human = person(human_nums)
        print_arms_blocking_head(human)
        if is_right_hook(human):
            return "hook"
        if is_left_hook(human):
            return "hook"
        elif are_arms_blocking_head(human):
            return "blocking"
        else:
            return "nothing"
    except:
        print("No human found")


#Used for debugging coordinates and stuff of the like

def print_arms_blocking_head(human):
    print("\tLeft Wrist: (" + str(human.body_parts[LWrist].x) + "," + str(human.body_parts[LWrist].y) + ")")
    print("\tRigt Wrist: (" + str(human.body_parts[RWrist].x) + "," + str(human.body_parts[RWrist].y) + ")")
    print("\tLeft Elbow: (" + str(human.body_parts[LElbow].x) + "," + str(human.body_parts[LElbow].y) + ")")
    print("\tRight Elbow: (" + str(human.body_parts[RElbow].x) + "," + str(human.body_parts[RElbow].y) + ")")
    print("\tNose: (" + str(human.body_parts[Nose].x) + "," + str(human.body_parts[Nose].y) + ")")
    print("####")


##########################Basic Coordinate Checks ##########################
#These are the basic x/y coordinate mapping estimation building blocks
def check_proximity(x, y, margin = .1):
    x1 = x - (x * margin)
    x2 = x + (x * margin)
    y1 = y - (y * margin)
    y2 = y + (y * margin)
    if x1 <= y <= x2 or y1 <= x <= y2:
        return True
    else:
        return False

####x and y axis in the API are inverted, I pretend to fix it here

def check_x_plane(body_part1, body_part2):
    return check_proximity(body_part1.y, body_part2.y)

def check_y_plane(body_part1, body_part2):
    return check_proximity(body_part1.x, body_part2.x)


def check_x_less(body_part1, body_part2):
    if body_part1.y < body_part2.y:
        return True
    else:
        return False
def check_y_less(body_part1, body_part2):
    #invert because the biggger the number the lower it is
    if body_part1.x < body_part2.x:
        return True
    else:
        return False


#Check whether body_part2 is between 1 & 3
def is_medial_x(body_part1, body_part2, body_part3):
    return in_range(body_part1.y, body_part2.y, body_part3.y)

def is_medial_y(body_part1, body_part2, body_part3):
    return in_range(body_part1.x, body_part2.x, body_part3.x)

def in_range(x, y, z):
    if x < z:
        if x < y < z:
            return True
        return False
    else:
        if z < y < x:
            return True
        return False


###########################################More Advanced Coordainte Maps###############
#These build on the other coordinate maps and make complicated decisions based on results

def are_knees_square(human):
    if check_x_plane(human.body_parts[LKnee],human.body_parts[RKnee]):
        print("Knees are square")

def are_shoulders_square(human):
    if check_x_plane(human.body_parts[LShoulder],human.body_parts[RShoulder]):
        print("Shoulders are square")

def is_right_arm_straight_down(human):
    if check_y_plane(human.body_parts[RShoulder],human.body_parts[RElbow]) \
        and check_y_plane(human.body_parts[RWrist],human.body_parts[RElbow]) \
            and check_x_less(human.body_parts[RWrist], human.body_parts[RElbow])\
                and check_x_less(human.body_parts[RElbow], human.body_parts[RShoulder]):
        print("Right Arm is straight down")

def is_left_arm_straight_down(human):
    if check_y_plane(human.body_parts[LShoulder],human.body_parts[LElbow]) \
        and check_y_plane(human.body_parts[LWrist],human.body_parts[LElbow]) \
            and check_x_less(human.body_parts[LWrist], human.body_parts[LElbow]) \
                and check_x_less(human.body_parts[LElbow], human.body_parts[LShoulder]):
        print("Left Arm is straight down")

def are_arms_blocking_head(human):
    if is_medial_y(human.body_parts[LElbow],human.body_parts[Nose],human.body_parts[RElbow]) \
        and is_medial_y(human.body_parts[LWrist], human.body_parts[Nose], human.body_parts[RWrist]) \
            and is_medial_x(human.body_parts[LWrist],human.body_parts[Nose],human.body_parts[LElbow]) \
                and is_medial_x(human.body_parts[RWrist],human.body_parts[Nose],human.body_parts[RElbow]):
        print("\t#############Face Block Detected###############")
        return True
    return False

def is_right_jab(human):
    if is_medial_y(human.body_parts[Nose],human.body_parts[RElbow],human.body_parts[RWrist]) \
        and check_x_plane(human.body_parts[Nose], human.body_parts[LWrist]):
        print("\t#############Right Jab Detected###############")
        return True
    else:
        return False

def not_null(part):
    if part.x > 0.0 and part.y > 0.0: return True
    else: 
        return False

def is_right_hook(human):
    if is_medial_y(human.body_parts[RShoulder],human.body_parts[RElbow],human.body_parts[RWrist]) \
        and check_x_less(human.body_parts[Nose], human.body_parts[RElbow]) \
            and not_null(human.body_parts[RElbow]) \
                and not_null(human.body_parts[RShoulder]) \
                    and not_null(human.body_parts[RWrist]) \
                        and check_y_less(human.body_parts[LElbow], human.body_parts[LWrist]):
        print("\t#############Right Hook Detected###############")
        return True
    else:
        return False

def is_left_hook(human):
    if is_medial_y(human.body_parts[LShoulder],human.body_parts[LElbow],human.body_parts[LWrist]) \
        and check_x_less(human.body_parts[Nose],human.body_parts[LElbow]) \
            and not_null(human.body_parts[LElbow]) \
                and not_null(human.body_parts[LShoulder]) \
                    and not_null(human.body_parts[LWrist]) \
                        and check_y_less(human.body_parts[RElbow], human.body_parts[RWrist]):
        print("\t#############Left Hook Detected###############")
        return True
    else:
        return False
