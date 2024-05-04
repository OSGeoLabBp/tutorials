#!/usr/bin/env python3

"""
    Simple demo YOLO object detection from webcam stream
"""

from sys import stdout
import argparse
import cv2
from ultralytics import YOLO

parser = argparse.ArgumentParser()
parser.add_argument('name', metavar='file_name', type=str, nargs=1,
                    help='video file to process or camera ID (e.g. 0)')
parser.add_argument('-s', '--show', action="store_true",
                    help='Show images with detected objects')
parser.add_argument('-o', '--output', type=str, default='stdout',
                    help='name of output file, default stdout')
parser.add_argument('-c', '--conf', type=float, default=0.1,
                    help='confidence level for acceptance, default: 0.1')
args = parser.parse_args()

model = YOLO("yolo-Weights/yolov8n.pt")

classNames = model.names
"""
['person', 'bicycle', 'car', 'motorbike', 'aeroplane', 'bus',
 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
 'donut', 'cake', 'chair', 'sofa', 'pottedplant', 'bed', 'diningtable',
 'toilet', 'tvmonitor', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
"""
if args.name[0] in ('0', '1', '2', '3'):
    cap = cv2.VideoCapture(int(args.name[0]))
    cap.set(3, 640)     # set camera resolution
    cap.set(4, 480)
else:
    cap = cv2.VideoCapture(args.name)
if args.output == 'stdout':
    of = stdout
else:
    of = open(args.output, 'w')

frame_id = 0
while True:
    ret, img = cap.read()   # get next frame from camera
    if not ret:
        break               # end of stream
    results = model(img, stream=True)   # YOLO object detection
    for r in results:
        boxes = r.boxes
        for box in boxes:
            if box.conf[0] < args.conf:
                continue
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]    # bounding box of detected object
            # print box, label and confidence
            print(f"{frame_id}:{int(x1)},{int(y1)},{int(x2)},{int(y2)}:{classNames[int(box.cls[0])]} {box.conf[0]:.1%}", file=of)
            if args.show:
                # draw rectangle and label on image
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 3)
                cv2.putText(img, f"{classNames[int(box.cls[0])]} {box.conf[0]:.1%}", (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    if args.show:
        cv2.imshow('Camera', img)
        if cv2.waitKey(1) == ord('q'):
            break
    frame_id += 1
cap.release()
cv2.destroyAllWindows()
