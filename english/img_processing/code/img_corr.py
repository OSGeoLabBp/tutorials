import cv2
import numpy as np
import sys

def img_correlation(img, templ):
    """ find most similar part to templ on img
         returns upper left corner of templ in img and statistic
    """
    rows, cols = img.shape
    trows, tcols = templ.shape
    row = col = None
    mins = trows * tcols * 255**2       # max statistic
    t = templ.astype(int)
    for i in range(rows - trows):
        i1 = i + trows
        for j in range(cols - tcols):
            j1 = j + tcols
            s = np.sum(np.square(t - img[i:i1, j:j1]))
            if s < mins:
                mins = s
                row = i
                col = j
    return (col, row, s)

try:
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    templ = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
except:
    print("Usage: img_corr image template")
    sys.exit()
print(img_correlation(img, templ))
