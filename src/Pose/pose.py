import argparse
import logging
import sys
import time

from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh


parser = argparse.ArgumentParser(description='tf-pose-estimation run')
parser.add_argument('--image', type=str)
model="mobilenet_thin"
args = parser.parse_args();

e = TfPoseEstimator(get_graph_path(model), target_size=(432, 368))
w, h = model_wh('0x0')
image = common.read_imgfile(args.image, None, None)
if image is None:
    logger.error('Image can not be read, path=%s' % args.image)
    sys.exit(-1)
resize_out_ratio=4.0
humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=resize_out_ratio)
image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)



cv2.imshow('result', image)
cv2.waitKey()

