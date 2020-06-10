import sys
import math

XMIN_INDEX = 0
YMIN_INDEX = 1
XMAX_INDEX = 2
YMAX_INDEX = 3


class Object:

    def __init__(self, default_life, bbox):
        self.default_life = default_life
        self.bbox = bbox
        self.origin_bbox = bbox
        self.resetLife()
        self.resetDuration()

    def resetLife(self):
        self.life = self.default_life

    def increaseLife(self):
        self.life += 1

    def decreaseLife(self):
        self.life -= 1

    def resetDuration(self):
        self.duration = 0

    def increaseDuration(self):
        self.duration += 1

    def decreaseDuration(self):
        self.duration -= 1

    def mergeBbox(self, bbox):
        self.bbox = merge_rects(self.bbox, bbox)


class ObjectManager:

    def __init__(self, default_life):
        self.default_life = default_life
        self.objects = []

    def setDefaultLife(self, v):
        self.default_life = v

    def setObjectsByBboxes(self, bboxes):
        self.objects = [self.convertBboxToObject(b) for b in bboxes]

    def getBboxes(self, min_duration=0):
        bboxes = []
        durations = []
        lifes = []
        for o in self.objects:
            if o.duration < min_duration:
                continue
            bboxes.append(o.bbox)
            durations.append(o.duration)
            lifes.append(o.life)
        return bboxes, durations, lifes

    def run(self, bboxes):
        if not self.objects:
            self.setObjectsByBboxes(bboxes)
            return

        new_objs = self.findNewObjects(bboxes)

        self.mergeObjects(bboxes)

        self.removeObjects()

        self.objects.extend(new_objs)

    def mergeObjects(self, bboxes):
        for o in self.objects:
            o.increaseDuration()
            exist = False
            for n in bboxes:
                if not compare(o.bbox, n):
                    continue

                exist = True
                o.resetLife()
                o.mergeBbox(n)

            if not exist:
                o.decreaseLife()

    def findNewObjects(self, bboxes):
        new_objs = []
        for n in bboxes:
            exist = False
            for o in self.objects:
                if not compare(o.bbox, n):
                    continue
                exist = True

            if not exist:
                new_objs.append(Object(self.default_life, n))
        return new_objs

    def removeObjects(self):
        remove = []
        for o in self.objects:
            if o.life <= 0:
                remove.append(o)
            elif not compare(o.origin_bbox, o.bbox):
                remove.append(o)

        for o in remove:
            self.objects.remove(o)

    def convertBboxToObject(self, bbox):
        return Object(self.default_life, bbox)


def get_rect(r):
    return [r[0], r[1], r[2], r[3]]


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
    # print(rect)
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


def compare_distance(old, new, standard, threshold):

    distance = distance_point_to_point(old, new)

    threshold_value = (1 - threshold) * standard

    # max_d = standard + threshold_value

    return True if distance <= threshold_value else False


def compare_side(old, new, threshold):
    threshold_value = (1 - threshold) * old

    min_size = old - threshold_value
    max_size = old + threshold_value

    return True if min_size <= new <= max_size else False


# [xmin, ymin, xmax, ymax, score, label]
def compare(old, new):

    center_distance_threshold = 0.9
    side_size_threshold = 0.95

    old_c = get_center(old)
    new_c = get_center(new)
    standard_distance = distance_point_to_point(
        [old[0], old[1]], [old[2], old[3]]) / 2

    old_w, old_h = get_size(old)
    new_w, new_h = get_size(new)

    if not compare_distance(old_c, new_c, standard_distance, center_distance_threshold):
        return False

    if not compare_side(old_w, new_w, side_size_threshold):
        return False

    if not compare_side(old_h, new_h, side_size_threshold):
        return False

    return True


def midpoint(p1, p2):
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    mx = math.floor((x1 + x2) / 2)
    my = math.floor((y1 + y2) / 2)
    return [mx, my]


def merge_rects(r1, r2):
    r1x1, r1y1, r1x2, r1y2 = get_rect(r1)
    r2x1, r2y1, r2x2, r2y2 = get_rect(r2)

    p1 = [r1x1, r1y1]
    p2 = [r2x1, r2y1]
    minx, miny = midpoint(p1, p2)

    p3 = [r1x2, r1y2]
    p4 = [r2x2, r2y2]
    maxx, maxy = midpoint(p3, p4)

    return [minx, miny, maxx, maxy]
