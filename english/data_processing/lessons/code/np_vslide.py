#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter point on a vertical section
    command line parameters: input_file, x1, y1, x2, y2, tolerance
    vertical plain is defined by (x1,y1) and (x2,y2)
"""
import sys
import numpy as np
from math import hypot

if len(sys.argv) < 7:
    print("usage: {} file x1 y1 x2 y2 tolerance\n".format(sys.argv[0]))
    sys.exit()
x1 = float(sys.argv[2])
y1 = float(sys.argv[3])
x2 = float(sys.argv[4])
y2 = float(sys.argv[5])
tol = float(sys.argv[6])
# set up equation for vertical plain vp[0] * x + vp[1] * y + vp[2] = 0
vp = np.zeros((3,))
vp[0] = y1 - y2
vp[1] = x2 - x1
vp[2] = x1 * y2 - x2 * y1
vp = vp / hypot(vp[0], vp[1])               # normalize
pc = np.loadtxt(sys.argv[1], delimiter=',') # load point cloud from text file
pc1 = pc.copy()
pc1[:, 2] = 1                   # change to homogenous 2D coord
sec = pc[np.dot(pc1, vp) < tol] # select points close to section
for i in range(sec.shape[0]):   # print out result
    print("{:.3f} {:.3f} {:.3f}".format(pc[i][0], pc[i][1], pc[i][2]))
