#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
    find template in image
"""
import cv2
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: %s method_id template image" % sys.argv[0])
        print("    method_id - 0/1/2/3 CV_TM_SQDIFF_NORMED/CV_TM_CCORR_NORMED/CV_TM_CCOEFF/CV_TM_CCOEFF_NORMED")
        print("    template  - template image to find in the video frames")
        print("    image     - image to process")
        exit(1)
    # selected method
    minv = 2    # index of min value
    maxv = 3    # index of max value
    methods = ((cv2.TM_SQDIFF_NORMED, minv), (cv2.TM_CCORR_NORMED, maxv),
        (cv2.TM_CCOEFF, maxv), (cv2.TM_CCOEFF_NORMED, maxv))
    method = methods[int(sys.argv[1])]
    # open template and convert to grayscale
    templ = cv2.imread(sys.argv[2])
    templ_gray = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
    # process image
    img = cv2.imread(sys.argv[3])
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray,templ_gray, method[0])
    min_max = cv2.minMaxLoc(result)
    x = min_max[method[1]][0]
    y = min_max[method[1]][1]
    w, h = templ.shape[:2]
    print(min_max[method[1]][1],min_max[method[1]][0])
    plt.figure()
    plt.title("template maching")
    plt.imshow(img)
    plt.plot(x, y, "o")
    rect = patches.Rectangle((x,y), h, w, linewidth=3, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)
    plt.show()
