#!/usr/bin/env python3

import cv2
import numpy as np
import sys

def img_correlation(img, templ):
    """ find most similar part to templ in img
        returns upper left corner of templ in image and statistic (square of differences)
    """
    rows, cols = img.shape              # image sizes
    trows, tcols = templ.shape          # template sizes
    row = col = None                    # for best match position
    mins = trows * tcols * 255**2       # initial value statistic

    for i in range(rows - trows):       # scan image rows
        i1 = i + trows                  # row for the bottom of template
        for j in range(cols - tcols):   # scan image columns
            j1 = j + tcols              # column for the right of template
            s = np.sum(np.square(templ - img[i:i1, j:j1]))  # pixel wise scatistic
            if s < mins:                # better statistic found?
                mins = s                # store the actual best match
                row = i
                col = j
    return (col, row, s)                # return position and statistic of best match

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} image_to_scan template_to_find')
        sys.exit()
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f'Image not found or failed to read: {sys.argv[1]}')
        sys.exit()
    templ = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    if templ is None:
        print(f'Template not found or failed to read: {sys.argv[2]}')
        sys.exit()
    print(img_correlation(img, templ))
