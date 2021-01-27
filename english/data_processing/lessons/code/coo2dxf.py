#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Read coordinates from file or standard input and write AutoCAD
    DXF to standard output
"""

from sys import (argv, stdin)

fp = stdin                      # use standard input or
if len(argv) > 1:
    fp = open(argv[1], 'r')     # file name from command line
# print mini DXF header
print("  0\nSECTION\n  2\nENTITIES")
for line in fp:
    fields = line.split()
    print("  0\nTEXT\n  8\nPTEXT\n 10\n{:.3f}\n 20\n{:.3f}\n 30\n0.0\n 40\n0.5".format(
        float(fields[1]) + 0.1, float(fields[2]) -0.25))
    print("  1\n{}\n 50\n0.0".format(fields[0]))
    print("  0\nPOINT\n  8\nPOINT\n 10\n{}\n 20\n{}\n 30\n{}".format(
        fields[1], fields[2], fields[3]))
# prinf dxf footer
print("  0\nENDSEC\n  0\nEOF")
