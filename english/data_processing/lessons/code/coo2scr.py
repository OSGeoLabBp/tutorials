#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Read coordinates from file or standard input and write AutoCAD
    script to standard output
"""

from sys import (argv, stdin)

fp = stdin                      # use standard input or
if len(argv) > 1:
    fp = open(argv[1], 'r')     # file name from command line
for line in fp:
    fields = line.split()
    print("TEXT {:.3f},{:.3f}".format(float(fields[1]) + 0.1,
                                     float(fields[2]) -0.25))
    print("0.25 0")         # text size and angle
    print(fields[0])        # text annotation
    print("POINT {},{},{}".format(fields[1], fields[2], fields[3]))
