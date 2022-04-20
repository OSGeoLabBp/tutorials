#! /usr/bin/python
# -*- coding: utf-8 -*-
"""
    go through video frames to find template and correlation
"""
import cv2
import sys

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} method_id template image1 [img2 ...]")
        print("    method_id - 0/1/2/3 CV_TM_SQDIFF_NORMED/CV_TM_CCORR_NORMED/CV_TM_CCOEFF/CV_TM_CCOEFF_NORMED")
        print("    template  - template image to find in the video frames")
        print("    image1")
        print("    image2    - images to process")
        exit(1)
    # selected method
    minv = 2    # index of min value
    maxv = 3    # index of max value
    methods = ((cv2.TM_SQDIFF_NORMED, minv), (cv2.TM_CCORR_NORMED, maxv),
        (cv2.TM_CCOEFF, maxv), (cv2.TM_CCOEFF_NORMED, maxv))
    method = methods[int(sys.argv[1])]
    # open template and convert to grayscale
    templ_gray = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    # process images
    for i in range(3, len(sys.argv)):
        img_gray = cv2.imread(sys.argv[i], cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(img_gray, templ_gray, method[0])
        min_max = cv2.minMaxLoc(result)
        print(i-2, min_max[method[1]])
