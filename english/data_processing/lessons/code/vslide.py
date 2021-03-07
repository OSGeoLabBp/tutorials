#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter points on a vertical section
    command line parameters: input_file, x1, y1, x2, y2, tolerance
    vertical plain is defined by (x1,y1) and (x2,y2)
"""
import sys
from math import hypot
import numpy as np

if len(sys.argv) < 7:
    print("usage: {} file x1 y1 x2 y2 tolerance\n".format(sys.argv[0]))
    sys.exit()
x1 = float(sys.argv[2])
y1 = float(sys.argv[3])
x2 = float(sys.argv[4])
y2 = float(sys.argv[5])
tol = float(sys.argv[6])
# set up equation for vertical plain a * x + b * y + c = 0
vp = np.zeros(3)
vp[0] = y1 - y2
vp[1] = x2 - x1
vp[2] = x1 * y2 - x2 * y1
# normalize
vp = vp / hypot(vp[0], vp[1])
print(vp)
mind = 1e38
with open(sys.argv[1]) as fp:
    for line in fp:
        p = [float(c) for c in line.strip().split(",")]
        if abs(np.dot(vp, np.array([p[0], p[1], 1]))) < tol:
            print("{:.3f},{:.3f},{:.3f}".format(p[0], p[1], p[2]))
