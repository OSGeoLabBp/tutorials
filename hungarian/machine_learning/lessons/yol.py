#!/usr/bin/env python3

"""
    Simple demo YOLO5 object detection from webcam stream
"""

import cv2
from ultralytics import YOLO

model = YOLO("yolo-Weights/yolov5n.pt")

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
cap = cv2.VideoCapture(0)
cap.set(3, 640)     # set camera resolution
cap.set(4, 480)

while True:
    ret, img = cap.read()   # get next frame from camera
    if not ret:
        break               # end of stream
    results = model(img, stream=True)   # YOLO object detection
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]    # bounding box of detected object
            # print box, label and confidence
            print(f"{int(x1)}, {int(y1)}, {int(x2)}, {int(y2)}: {classNames[int(box.cls[0])]} {box.conf[0]:.1%}")
            # draw rectangle and label on image
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 255), 3)
            cv2.putText(img, classNames[int(box.cls[0])], (int(x1), int(y1)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Cam', img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
