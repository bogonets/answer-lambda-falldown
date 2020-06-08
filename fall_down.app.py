# -*- coding: utf-8 -*-

import numpy as np
import time
import sys
import math

maximum = 0
seconds = [1]
labels = ['Occur1']
estimation_count = [1]
interval_sec = [1]

last_estimated_times = []
input_times = []

old_obj = []

center_distance_threshold = 0.5
side_size_threshold = 0.5

XMIN_INDEX = 0
YMIN_INDEX = 1
XMAX_INDEX = 2
YMAX_INDEX = 3


def get_center(rect):
    x1 = rect[XMIN_INDEX]
    y1 = rect[YMIN_INDEX]
    x2 = rect[XMAX_INDEX]
    y2 = rect[YMAX_INDEX]

    w = x2 - x1
    h = y2 - y1

    cx = x1 + int(w / 2)
    cy = y1 + int(h / 2)
    return (cx, cy)


def get_size(rect):
    x1 = rect[XMIN_INDEX]
    y1 = rect[YMIN_INDEX]
    x2 = rect[XMAX_INDEX]
    y2 = rect[YMAX_INDEX]

    w = x2 - x1
    h = y2 - y1
    return w, h


def distance_point_to_point(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance


# [xmin, ymin, xmax, ymax, score, label]
def compare_distance(old, new, threshold):

    distance = distance_point_to_point(old, new)

    return True if distance >= threshold else False


def compare_side(old, new, threshold):
    ds = old - new
    distance = math.sqrt(d**2)

    return True if distance >= threshold else False


def compare(old, new):

    center_distance_threshold = 0.5
    side_size_threshold = 0.5

    old_c = get_center(old)
    new_c = get_center(new)

    if not compare_distance(old_c, new_c, center_distance_threshold):
        return False

    old_w, old_h = get_size(old_c)
    new_w, new_h = get_size(new_c)

    if not compare_side(old_w, new_w, side_size_threshold):
        return False

    if not compare_side(old_h, new_h, side_size_threshold):
        return False

    return True


def compare_in_exists(olds):
    idx = 1
    for i in range(len(olds) - 1):
        for k in range(idx, len(olds)):
            compare(i, k)


def on_run(array):

    if not old_obj:
        old_obj = array.tolist()
        return {'result': np.array()}

    for o in old_obj:
        for n in array:
            compare(o, n)

    return {
        'result': np.array([condition_result], np.int32)}


def on_destroy():
    return True


if __name__ == '__main__':
    pass
