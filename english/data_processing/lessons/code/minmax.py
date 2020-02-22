#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" find min and max values in a column of an ascii pointcloud file
    command line parameters: column_number input_file
"""
import sys

if len(sys.argv) < 3:
    print("usage: {} column_number file\n".format(sys.argv[0]))
    sys.exit()
min = 1e38
max = -min
col = int(sys.argv[1]) - 1  # shift column number to zero based
with open(sys.argv[2]) as fp:
    for line in fp:
        fields = [float(c) for c in line.strip().split(",")]
        if fields[col] < min: min = fields[col] 
        if fields[col] > max: max = fields[col]

print("{:.3f} {:.3f}".format(min, max))
