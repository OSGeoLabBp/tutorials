import cv2
import sys

if len(sys.argv) > 1:
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    cv2.imwrite("canny.png", cv2.Canny(img, 200, 300))
