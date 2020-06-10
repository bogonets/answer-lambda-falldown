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


def compare_in_exists(olds):
    idx = 1
    for i in range(len(olds) - 1):
        exist_similar = False
        for k in range(idx, len(olds)):
            if not compare(i, k):
                continue

            
            
            break


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
