#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter point on a section perpendicular to an axis
    command line parameters: input_file, section_coordinate, column, tolerance 
    e.g. a horizontal section at 1000 meter: np_slide.py lidar.txt 1000 3 0.1
"""
import sys
import numpy as np

if len(sys.argv) < 5:
    print("usage: {} file section column tolerance\n".format(sys.argv[0]))
    sys.exit()
coo = float(sys.argv[2])    # section coordinate
col = int(sys.argv[3]) - 1  # shift column number to zero based
tol = float(sys.argv[4])

pc = np.loadtxt(sys.argv[1], delimiter=',') # load point cloud from text file
sec = pc[np.absolute(pc[:, col] - coo) < tol]   # select points near to section
for i in range(sec.shape[0]):               # print out result
    print("{:.3f} {:.3f} {:.3f}".format(sec[i][0], sec[i][1], sec[i][2]))
