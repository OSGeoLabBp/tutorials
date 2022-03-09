#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from math import hypot
import numpy as np
from matplotlib import pyplot as plt

def vplain(x1, y1, x2, y2):
    """ set up line equation
    vp[0] * x + vp[1] * y + vp[2] = 0

    x1, y1 - horizontal coordinates of the start point of the section
    x2, y2 - horizontal coordinates of the end point of the section
    returns a numpy array with coefficients of the vertical plane
    """

    vp = np.zeros((3,))
    vp[0] = y1 - y2
    vp[1] = x2 - x1
    vp[2] = x1 * y2 - x2 * y1
    vp = vp / hypot(vp[0], vp[1]) # normalize
    return vp

def section(pc, x1, y1, x2, y2, tol):
    """ Select point from a point cloud near to a line

    pc - point cloud in a numpy array
    x1, y1 - horizontal coordinates of the start point of the section
    x2, y2 - horizontal coordinates of the end point of the section
    tol - tolerance distance from the section
    returns a numpy array with points near to the section
    """
    pc1 = pc.copy()
    pc1[:, 2] = 1 # change to homogenous coordinates
    vp = vplain(x1, y1, x2, y2) # equation of vertical plain
    sec = pc[np.abs(np.dot(pc1, vp)) < tol] # select points close to the section

    return sec

def tr(e1, n1, e2, n2):
    """ set up transformation matrix for homogenous coordinates

    Parameters:
    e1, n1 - start point of the section line
    e2, n2 - end point of the section section line
    returns the transformation matrix
    """
    de = e2 - e1
    dn = n2 - n1

    d = hypot(de, dn) # distance
    r = de / d # sin
    m = dn / d # cos
    return np.dot(np.array([[1, 0, 0], [0, 1, 0], [-e1, -n1, 1]]),
                np.array([[m, r, 0], [-r, m, 0], [0, 0, 1]]))

if len(sys.argv) < 7:
  pc = np.loadtxt('sample_data/lidar.txt', delimiter=',') ;# load point cloud
  x1 = 548060.0
  y1 = 5129130.0
  x2 = 255130.0
  y2 = 5129030.0
  tol = 1.0
else:
    pc = np.loadtxt(sys.argv[1], delimiter=',') ;# load point cloud
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])
    tol = float(sys.argv[6])
# set up equation for vertical plain a * x + b * y + c = 0
vp = vplain(x1, y1, x2, y2)
mind=1e38
sec = section(pc,x1,y1,x2,y2,tol) 
# transformation matrix
trm = tr(x1, y1, x2, y2)
# make a copy of section points for homogenous transformation
pc1 = sec.copy()
pc1[:, 2] = 1
pc1 = np.dot(pc1, trm) # rotate points into the section plain
pc1[:, 2] = sec[:, 2] # copy back elevations to transformed points

plt.plot(pc1[:,1], pc1[:,2], 'o')
plt.xlabel('chainage (m)')
plt.ylabel('elevation (m)')
plt.axis('equal')
plt.grid('on')
plt.show() 
