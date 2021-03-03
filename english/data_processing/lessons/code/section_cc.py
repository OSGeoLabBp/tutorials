#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" get vertical section of a point cloud using command line interface of CloudCompare
    command line parameters: input_file, e1, n1, e2, n2, tolerance
    e.g. python section_cc.py pc_ftszv_5cm.txt 660125.48 230851.85 660128.75 230835.43 0.20
"""
import sys
import math
import subprocess
import platform

if len(sys.argv) < 7:
    print("usage: {} file e1 n1 e2 n2 tolerance\n".format(sys.argv[0]))
    sys.exit()

# easting and northing of 1st and 2nd points on section    
e1 = float(sys.argv[2])
n1 = float(sys.argv[3])
e2 = float(sys.argv[4])
n2 = float(sys.argv[5])
tol = float(sys.argv[6]) 

# coordinate differences
de = e2 - e1
dn = n2 - n1
#distance
d = math.sqrt(de**2 + dn**2)
# sinus/cosinus of the whole circle bearing
r=de/d
m=dn/d

# 1st corner of the rectangle
ep1 = e1 - r - tol * m
np1 = n1 - m + tol * r

# 2nd corner of the rectangle
ep2 = e1 + d * r - tol * m
np2 = n1 + d * m + tol * r

# 3rd corner of the rectangle
ep3 = e1 + d * r + tol * m
np3 = n1 + d * m - tol * r

# 4th corner of the rectangle
ep4 = e1 - r + tol * m
np4 = n1 - m - tol * r

# check platform
if platform.system() is 'Windows':
   cc = "C:\Program Files\CloudCompare\CloudCompare.exe"
elif platform.system() is 'Linux':
   cc = "cloudcompare.CloudCompare"
else:
   print("you can use CC on windows or linux")
   sys.exit()

# run CC command
subprocess.run([cc, "-SILENT", "-O", sys.argv[1], "-C_EXPORT_FMT", "ASC",
    "-PREC", "3", "-Crop2d", "Z", "4", str(ep1), str(np1), str(ep2), str(np2),
    str(ep3), str(np3), str(ep4), str(np4)])
