# -*- coding: utf-8 -*-

import numpy as np
import time
import sys
import math
import falldown

obj_manager = None

falldown_frame_count = 60
min_keep_frame = 15
center_distance_threshold = 0.9
side_size_threshold = 0.95


def on_set(k, v):
    if k == 'falldown_frame_count':
        global falldown_frame_count
        falldown_frame_count = int(v)
    elif k == 'min_keep_frame':
        global min_keep_frame
        min_keep_frame = int(v)
    elif k == 'center_distance_threshold':
        global center_distance_threshold
        center_distance_threshold = float(v)
    elif k == 'side_size_threshold':
        global side_size_threshold
        side_size_threshold = float(v)


def on_get(k):
    if k == 'falldown_frame_count':
        return str(falldown_frame_count)
    elif k == 'min_keep_frame':
        return str(min_keep_frame)
    elif k == 'center_distance_threshold':
        return str(center_distance_threshold)
    elif k == 'side_size_threshold':
        return str(side_size_threshold)


def on_init():
    global obj_manager
    obj_manager = falldown.ObjectManager(min_keep_frame, center_distance_threshold, side_size_threshold)
    return True


def on_run(bboxes):

    obj_manager.run(bboxes)

    falldown_bboxes, durations, lifes = obj_manager.getBboxes(falldown_frame_count)

    # sys.stdout.write(f"[fall_down] falldown_bboxes {falldown_bboxes} {type(falldown_bboxes)}\n")
    # sys.stdout.flush()

    return {
        'result': np.array(falldown_bboxes)
        }


def on_destroy():
    return True

