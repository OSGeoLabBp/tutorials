# -*- coding: utf-8 -*-
"""
    RANSAC line demonstration in 2D

    usage:
       ransac_line.py tolerance iterations all_img random_seed show

       tolerance - max distance from point to line to accept, float, default 5
       iterations - number of iterations, int, default 100
       all_img - if 0 only best solutions are shown, otherwise all, int, default 0
       random_seed - seed for random number, int, 5 is a good solution!!!!
       show - show results on screen 0/1, int, default 0
"""

import sys
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt

# parameters
tolerance = 5       # distance from the plane to accept point
iterations = 100    # number of iterations
all_img = 0         # show all attempts
show = 0

if len(sys.argv) > 1:
    tolerance = float(sys.argv[1])
if len(sys.argv) > 2:
    iterations = int(sys.argv[2])
if len(sys.argv) > 3:
    all_img = int(sys.argv[3])
if len(sys.argv) > 4:
    np.random.seed(int(sys.argv[4]))
if len(sys.argv) > 5:
    show =  int(sys.argv[5])

n = 100 # number of inliers
k = 300  # number of outliers
range = 100.0   # range of x, y coordinates from zero to range
l = [0.451, -1.0, 2.0]  # line equation ax + by + c = 0
x = np.zeros(n+k)
y = np.zeros(n+k)
# points near to the line y = mx+b
x[:n] = np.random.rand(n) * range
y[:n] = -l[0] / l[1] * x[:n] - l[2] / l[1] + (np.random.rand(n) * tolerance - tolerance / 2)
x[n:] = np.random.rand(k) * range
y[n:] = np.random.rand(k) * range
points = np.c_[x, y, np.full(n+k, 1.0)]

fig = plt.figure()
ax = fig.add_subplot()
ax.scatter(x, y)
#ax.plot([0,100], [-l[2] / l[1], -l[0] / l[1] * 100 - l[2] / l[1]], 'r', label='original line')
_ = ax.set_title('Pontok')
ax.set_xlim((-2, 102))
ax.set_ylim((-2, 102))
plt.savefig('rl000.png')
if show:
    plt.show()
else:
    plt.close()

best_n = 0          # number of points on the best fit line so far
best_i = 0          # iteration index of best fit line so far
best_inliers = np.array([]) # indices of inliers of the best fit line so far
for i in np.arange(1, iterations):
    # select two random points
    p = []  # list of random indices for points
    while len(p) != 2:
        p = list(set(np.random.randint(n+k, size=2))) # remove repeated random integers
    p1 = points[p]  # randomly selected points
    x1 = p1[:,0]    # x coordinates
    y1 = p1[:,1]    # y coordinates
    # line equation from the two points using homogenouos coordinates
    l1 = np.array([y1[0] - y1[1], x1[1] - x1[0], x1[0] * y1[1] - x1[1] * y1[0]])
    l1 = l1 / sqrt(l1[0]**2 + l1[1]**2)     # normalize
    # select close points
    inliers = points[np.abs(np.dot(points, l1)) < tolerance]
    if inliers.shape[0] > best_n:
        # better solution found
        best_n = inliers.shape[0]
        best_i = i
        print(i, best_n)
        best_inliers = inliers[:,:2].copy()
        best_line = l1.copy()
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter(x, y)
        ax.scatter(best_inliers[:,0], best_inliers[:,1], c='g')
        ax.plot([0,100], [-best_line[2] / best_line[1], -best_line[0] / best_line[1] * 100 - best_line[2] / best_line[1]], color='red')
        _ = ax.set_title(f'{i}. iterráció {best_n} pont, új optimum')
        ax.set_xlim((-2, 102))
        ax.set_ylim((-2, 102))
        plt.savefig(f'rl{i:03d}.png')
        if show:
            plt.show()
        else:
            plt.close()
    elif all_img:
        act_n = inliers.shape[0]
        print(i, act_n)
        act_inliers = inliers[:,:2].copy()
        act_line = l1.copy()
        fig = plt.figure()
        ax = fig.add_subplot()
        ax.scatter(x, y)
        ax.scatter(act_inliers[:,0], act_inliers[:,1], c='y')
        ax.plot([0,100], [-act_line[2] / act_line[1], -act_line[0] / act_line[1] * 100 - act_line[2] / act_line[1]], color='magenta', linestyle='dashed')
        _ = ax.set_title(f'{i}. iterráció {act_n} pont')
        ax.set_xlim((-2, 102))
        ax.set_ylim((-2, 102))
        plt.savefig(f'rl{i:03d}.png')
        if show:
            plt.show()
        else:
            plt.close()

print(f'Best solution after {best_i} iterations, {best_n} points on line: {best_line}')

#fig = plt.figure()
#ax = fig.add_subplot()
#ax.scatter(x, y)
#ax.plot([0,100], [-best_line[2] / best_line[1], -best_line[0] / best_line[1] * 100 - best_line[2] / best_line[1]], 'r', label='best line')
#_ = ax.set_title('RANSAC line')
#plt.show()
