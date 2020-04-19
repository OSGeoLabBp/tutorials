import cv2
import sys
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    img2 = cv2.Canny(img, 200, 300)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle('Canny'
    ax1.imshow(img)
    ax2.imshow(img2)
    fig.show()
    input()
    cv2.imwrite("canny.png", img2)
