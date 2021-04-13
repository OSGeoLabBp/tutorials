import cv2
import numpy as np
import os.path
from sys import argv

if len(argv) < 2:
    print("Usage: {} img_file [img_file ...]".format(argv[0]))
    exit()

# process images
for fn in argv[1:]:
    img = cv2.imread(fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 120)
    minLineLength = 20
    maxLineGap = 5
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength, maxLineGap)
    for line in lines:
        for x1, y1, x2, y2 in line:
            print(x1, y1, x2, y2)
            cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), 8)
    fn1 = os.path.split(fn)
    fn2 = os.path.join(fn1[0], "e_" + fn1[1])
    fn3 = os.path.join(fn1[0], "l_" + fn1[1])
    cv2.imwrite(fn2, edges)
    cv2.imwrite(fn3, img)

    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.imshow('edges', edges)
    cv2.waitKey(0)
