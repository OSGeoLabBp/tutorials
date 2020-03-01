import sys
import math
import numpy as np

if len(sys.argv) > 1:
    fn = sys.argv[1]
else:
    fn = 'circletest.txt'
x1 = []
y1 = []
# load x,y data from file into lists
with open(fn, 'r') as fp:
    for line in fp:
        l = line.strip().split()
        x1.append(float(l[0]))
        y1.append(float(l[1]))
x = np.array(x1)        # create numpy array from x coords
y = np.array(y1)        # create numpy array from y coords
b = -(x * x + y * y)    # create pure terms
ones = np.array([1.0] * np.size(x)) # build coefficient matrix
a = np.append(x, y)
a = np.append(a, ones)
# solve least squares
par = np.linalg.lstsq(a.reshape(3, np.size(x)).T, b)
# get original variables
xc = -0.5 * par[0][0]
yc = -0.5 * par[0][1]
R = math.sqrt((par[0][0] ** 2 + par[0][1] ** 2) / 4.0 - par[0][2])
print('{:.3f} {:.3f} {:.3f}'.format(xc, yc, R))
