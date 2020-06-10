import sys
import os
import cv2

import falldown


def main(image_dir):
    files = os.listdir(image_dir)

    test_files = list(filter(lambda x: x.split('_')[0] == 'im', files))
    jpgs = list(filter(lambda x: x.split('.')[-1] == 'jpg', test_files))

    jpgs.sort()
    if not jpgs:
        print("Could not found files!")
        return

    index = 0
    max_index = len(jpgs) - 1

    obj_manager = utils.ObjectManager(15)

    while True:

        jp = os.path.join(image_dir, jpgs[index])
        tp = toTxtFile(jp)
        contents = getTxtContents(tp)

        bboxes = eval(contents)

        img = cv2.imread(jp)

        # BBOX
        # print(bboxes)
        bb_img = img.copy()
        for bb in bboxes:
            bb_img = cv2.rectangle(bb_img, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), (0, 0, 255), 3)


        # Objects
        obj_manager.run(bboxes)

        bboxes, durations, lifes = obj_manager.getBboxes()

        print(bboxes)
        print(durations)
        print(lifes)

        obj_img = img.copy()
        for bb, d, l in zip(bboxes, durations, lifes):
            obj_img = cv2.rectangle(obj_img, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), (0, 255, 0), 3)

        bboxes, durations, lifes = obj_manager.getBboxes(60)
        for bb, d, l in zip(bboxes, durations, lifes):
            obj_img = cv2.rectangle(obj_img, (int(bb[0]), int(bb[1])), (int(bb[2]), int(bb[3])), (0, 0, 255), 3)

        cv2.imshow('ori', img)
        cv2.imshow('bb_img', bb_img)
        cv2.imshow('obj_img', obj_img)

        key = cv2.waitKey(0)

        if key == 27:
            break
        elif key == ord('q'):
            if index > 0:
                index -= 1
            else:
                index = 0
        elif key == ord('e'):
            if index < max_index:
                index += 1
            else:
                index = max_index
        # elif key == ord('z'):


def toTxtFile(p):
    base = ''.join(p.split('.')[:-1])
    return base + '.txt'


def getTxtContents(txt):
    contents = ''
    with open(txt, 'r') as f:
        contents = f.read()
    return contents


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} IMAGE_DIR")
        exit(1)
    main(sys.argv[1])
