#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filterr point on a section perpendicular to an axis
    command line parameters: input_file, section_coordinate, column, tolerance 
"""
import sys

if len(sys.argv) < 5:
    print("usage: {} file section column tolerance\n".format(sys.argv[0]))
    sys.exit()
coo = float(sys.argv[2])
col = int(sys.argv[3]) - 1  # shift column number to zero based
tol = float(sys.argv[4])

with open(sys.argv[1]) as fp:
    for line in fp:
        fields = [float(c) for c in line.strip().split(",")]
        if abs(fields[col] - coo) < tol:
            print("{:.3f},{:.3f},{:.3f}".format(fields[0], fields[1], fields[2]))
