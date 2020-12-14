import argparse
import logging
import time
import matplotlib.pyplot as plt
import cv2
import numpy as np
import slidingwindow as sw
import tensorflow as tf
import time
from tf_pose import common
from tf_pose.common import CocoPart
from tf_pose.common import CocoPart as body_parts
from tf_pose.tensblur.smoother import Smoother
import tensorflow.contrib.tensorrt as trt
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

#preset constants, DO NOT CHANGE
Nose = 0
Neck = 1
RShoulder = 2
RElbow = 3
RWrist = 4
LShoulder = 5
LElbow = 6
LWrist = 7
RHip = 8
RKnee = 9
RAnkle = 10
LHip = 11
LKnee = 12
LAnkle = 13
REye = 14
LEye = 15
REar = 16
LEar = 17
Background = 18
##############################Coordinate Debugging###############
#Used for debugging coordinates and stuff of the like
def print_humans_info(humans):
        for human in humans:
            if human.part_count() > 14:# have only complete figures or near complete figures
                print("For Human: ")
                for i in range(common.CocoPart.Background.value):
                    if i not in human.body_parts.keys():
                        continue
                    body_part = human.body_parts[i]
                    print("\t" + str(body_part.get_part_name()) + "::" + str(body_part.part_idx) + "::" + " ----X: " + str(body_part.x) + " Y: " + str(body_part.y))
def print_arms_blocking_head(human):
        print("Left Wrist: (" + str(human.body_parts[LWrist].y) + "," + str(human.body_parts[LWrist].x) + ")")
        print("Rigt Wrist: (" + str(human.body_parts[RWrist].y) + "," + str(human.body_parts[RWrist].x) + ")")
        print("Left Elbow: (" + str(human.body_parts[LElbow].y) + "," + str(human.body_parts[LElbow].x) + ")")
        print("Right Elbow: (" + str(human.body_parts[RElbow].y) + "," + str(human.body_parts[RElbow].x) + ")")
        print("Nose: (" + str(human.body_parts[Nose].y) + "," + str(human.body_parts[Nose].x) + ")")

def parse_humans(humans):
    if len(humans) > 1:
        print("Humans are multiple")
    elif len(humans) == 1:
        print("Human is one")
    return len(humans)

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
    if body_part1.x > body_part2.x:
        return True
    else:
        return False
def check_x_less(body_part1, body_part2):
    #invert because the biggger the number the lower it is
    if body_part1.y > body_part2.y:
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
    if check_y_plane(human.body_parts[RShoulder],human.body_parts[RElbow]) and check_y_plane(human.body_parts[RWrist],human.body_parts[RElbow]) and check_x_less(human.body_parts[RWrist], human.body_parts[RElbow]) and check_x_less(human.body_parts[RElbow], human.body_parts[RShoulder]):
        print("Right Arm is straight down")
def is_left_arm_straight_down(human):
    if check_y_plane(human.body_parts[body_parts.LShoulder.value],human.body_parts[body_parts.LElbow.value]) and check_y_plane(human.body_parts[body_parts.LWrist.value],human.body_parts[body_parts.LElbow.value]) and check_x_less(human.body_parts[LWrist], human.body_parts[LElbow]) and check_x_less(human.body_parts[LElbow], human.body_parts[LShoulder]):
        print("Left Arm is straight down")
def are_arms_blocking_head(human):
        if is_medial_y(human.body_parts[LElbow],human.body_parts[Nose],human.body_parts[RElbow]) and is_medial_y(human.body_parts[LWrist], human.body_parts[Nose], human.body_parts[RWrist]) and is_medial_x(human.body_parts[LWrist],human.body_parts[Nose],human.body_parts[LElbow]) and is_medial_x(human.body_parts[RWrist],human.body_parts[Nose],human.body_parts[RElbow]):
                print("Human is blocking face")
                return True
        return False
