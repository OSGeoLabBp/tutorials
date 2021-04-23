#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter point on a vertical section
    command line parameters: input_file, x1, y1, x2, y2, tolerance
    vertical plain is defined by (x1,y1) and (x2,y2)
"""
import sys
import os.path
import psutil
import numpy as np
from math import hypot

def section(pc, vp, tol):
    """ select points on a vertical plan defined by vp

        :param pc: array for x,y,z coordinates of points
        :param vp: vertival plan vp[0] * x " vp[1] * y + vp[2] = 0
        :param tol: tolerance distance from plan
        :returns: select point in a numpy array
    """
    pc1 = pc.copy()
    pc1[:, 2] = 1                   # change to homogenous 2D coord
    sec = pc[np.abs(np.dot(pc1, vp)) < tol] # select points close to section
    return sec

def print_points(pc, decimals):
    """ print coordinates to the standard output

        :param pc: numpy array with coordinates (n, 3)
    """
    fmt = (("{:." + str(decimals) + "f} ") * 3).strip()
    for i in pc:   # print out result
        print(fmt.format(i[0], i[1], i[2]))

if len(sys.argv) < 7:
    print("usage: {} file x1 y1 x2 y2 tolerance\n".format(sys.argv[0]))
    sys.exit()
x1 = float(sys.argv[2])
y1 = float(sys.argv[3])
x2 = float(sys.argv[4])
y2 = float(sys.argv[5])
tol = float(sys.argv[6])
# set up equation for vertical plan vp[0] * x + vp[1] * y + vp[2] = 0
vp = np.array([y1 - y2, x2 - x1, x1 * y2 - x2 * y1], dtype=float)
vp = vp / hypot(vp[0], vp[1])               # normalize line equation
chunk = psutil.virtual_memory().available // 2
if os.path.getsize(sys.argv[1]) > chunk:
    # read in chunks
    with open(sys.argv[1], 'r') as fp:
        while True:
            lines = fp.readlines(chunk)
            if len(lines) == 0:
                break
            pc = np.zeros((len(lines), 3))
            for i, line in enumerate(lines):
                l = line.split(',')
                pc[i, 0] = float(l[0])
                pc[i, 1] = float(l[1])
                pc[i, 2] = float(l[2])
            print_points(section(pc, vp, tol), 3)
else:
    pc = np.loadtxt(sys.argv[1], delimiter=',') # load point cloud from text file
    pc = pc[:,0:3]      # remove extra columns
    print_points(section(pc, vp, tol), 3)
