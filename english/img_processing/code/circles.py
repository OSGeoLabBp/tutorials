import cv2
import numpy as np
import os.path
from sys import argv

if len(argv) < 2:
    print("Usage: {} img_file [img_file ...]".format(argv[0]))
    exit()

# process images
for fn in argv[1:]:
    try:
        src_img = cv2.imread(fn)    # load image
    except:
        print("Failed to read image {}".format(fn))
        continue
    # convert image to gray scale
    gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
    # noise reduction
    img = cv2.medianBlur(gray_img, 5)
    #find circles
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 400,
                            param1=100, param2=30, minRadius=10, maxRadius=1000)
    print circles
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(src_img, (i[0], i[1]), i[2], (0, 255, 0), 10)
        # draw the center of the circle
        cv2.circle(src_img, (i[0], i[1]), 2, (0,0,255), 10)
        fn1 = os.path.split(fn)
        fn2 = os.path.join(fn1[0], "c_" + fn1[1])
        cv2.imwrite(fn2, src_img)
