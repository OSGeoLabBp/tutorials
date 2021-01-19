import csv
import numpy as np
import matplotlib.pyplot as plt
from sys import argv
from math import (sin, cos, atan2, pi)

if len(argv) > 1:
    # load data from file
    x = []
    y = []
    with open(argv[1]) as csvin:
        reader = csv.reader(csvin, delimiter=' ')
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    X = np.array(list(zip(x, y)))
else:
    # generating normal distribution 2D point set with mean (0,0)
    X = np.random.multivariate_normal([0, 0], [[10, 5], [5, 100]], 500)
    # transform points (rotate and shift)
    alpha = -pi / 3.
    rot = np.array([[cos(alpha), sin(alpha)], [-sin(alpha), cos(alpha)]])
    X = X.dot(rot) + np.array([10, 20])
means = np.mean(X, 0)   # mean of coordinates
Xd = X - means          # differences from mean point
cov = Xd.T.dot(Xd)      # variance covariance matrix
eig_values, eig_vectors = np.linalg.eig(cov)
# principal direction is the first eigenvector
direction = atan2(eig_vectors[0][0], eig_vectors[1][0]) * 180 / pi # bearing
print('weight point: {}'.format(means))
print('direction [degree]: {:.1f}'.format(direction))
# plot points and axles
X1 = np.array([means[0], means[0] + eig_vectors[0][0] * eig_values[0] / 500.])
Y1 = np.array([means[1], means[1] + eig_vectors[1][0] * eig_values[0] / 500.])
X2 = np.array([means[0], means[0] + eig_vectors[0][1] * eig_values[1] / 500.])
Y2 = np.array([means[1], means[1] + eig_vectors[1][1] * eig_values[1] / 500.])
plt.plot(X[:,0], X[:,1], 'o')
plt.plot(X1, Y1, linewidth=3)
plt.plot(X2, Y2, linewidth=3)
plt.axis('equal')
plt.show()
