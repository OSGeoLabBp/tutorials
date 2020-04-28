import cv2 as cv
import numpy as np
import math
import matplotlib.pyplot as plt

# get the image
img = cv.imread('monalisa.jpg')
rows, cols, bands = img.shape
# set circular kernel
kernel = np.array([[0, 0, 1, 0, 0],
                   [0, 1, 1, 1, 0],
                   [1, 1, 1, 1, 1],
                   [0, 1, 1, 1, 0],
                   [0, 0, 1, 0, 0]])
n = kernel.shape[0]         # kernel size, should be odd number
n2 = n * n                  # items in kernel
n1 = np.sum(kernel)         # number of 1s in kernel
bord = n // 2               # skipped border area
bord1 = n // 2 + 1
res = np.empty(img.shape, dtype='uint8')   # empty byte array for stdev
res1 = np.empty(img.shape, dtype='uint8')  # empty byte array for means
for band in range(bands):
   for y in range(bord, rows - bord):
        for x in range(bord, cols - bord):
            part = img[y-bord:y+bord1, x-bord:x+bord1, band]
            mean = np.sum(part * kernel) / n1   # averages of none zero kernel
            res1[y, x, band] = int(mean + 0.5)
            stddev = math.sqrt(np.sum(((part - mean) * kernel)**2) / (n1 - 1))
            res[y, x, band] = int(stddev + 0.5)
 
plt.figure()
plt.title('smoothed image')
plt.imshow(res1)
plt.show()
plt.figure()
plt.title('stddev of image')
plt.imshow(res)
plt.show()
