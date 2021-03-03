#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" get vertical sections of a point cloud using command line interface of CloudCompare
    section points are stored in a file
    command line parameters: point_cloud_file, section_points_file, tolerance
    e.g. python section_cc_file.py PointCloud_2020_04_30-09_27_19-15cm.ply metszetsikok.csv 0.20
"""
import sys
import math
import subprocess
import platform
import os
import glob

if len(sys.argv) < 3:
    print("usage: {} point_cloud_file section_points_file tolerance\n".format(sys.argv[0]))
    sys.exit()

#point cloud filename without extension
fname = os.path.splitext(sys.argv[1])[0]

# check platform
if platform.system() == 'Windows':
    cc = "C:\Program Files\CloudCompare\CloudCompare.exe"
    #delete all the files with the point cloud filename but with extension asc
    fileList = glob.glob(fname + '*.asc')
    for f in fileList:
        os.remove(f)
elif platform.system() == 'Linux':
    cc = "cloudcompare.CloudCompare"
else:
    print("you can use CC on windows or linux")
    sys.exit()

#print out CC command   
#print(cc)

#tolerance
tol = float(sys.argv[3])

#read section_points_file, file structure
#station;e1;n1;e2;n2
with open(sys.argv[2]) as fp:
    for line in fp:
        fields = [float(c) for c in line.strip().split(";")]
        # easting and northing of 1st and 2nd points on section
        e1 = fields[1]
        n1 = fields[2]
        e2 = fields[3]
        n2 = fields[4]

        # coordinate differences
        de = e2 - e1
        dn = n2 - n1
        #distance
        d = math.hypot(de, dn)
        # sinus/cosinus of the whole circle bearing
        r = de / d
        m = dn / d

        # 1st corner of the rectangle
        ep1 = e1 - tol * m
        np1 = n1 + tol * r

        # 2nd corner of the rectangle
        ep2 = e1 + d * r - tol * m
        np2 = n1 + d * m + tol * r

        # 3rd corner of the rectangle
        ep3 = e1 + d * r + tol * m
        np3 = n1 + d * m - tol * r

        # 4th corner of the rectangle
        ep4 = e1 + tol * m
        np4 = n1 - tol * r

        #print out coordinates
        #print('{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}'.format(ep1, np1, ep2, np2, ep3, np3, ep4, np4))

        # run CC command
        subprocess.run([cc, "-SILENT", "-O", sys.argv[1], "-C_EXPORT_FMT", "ASC",
            "-PREC", "3", "-Crop2d", "Z", "4", str(ep1), str(np1), str(ep2), str(np2),
            str(ep3), str(np3), str(ep4), str(np4)])
        #CC automatically gives output filename
        outpf_cc = glob.glob(fname + '*.asc')
        #new filaname, first item in the section file
        outp = "{:.0f}.asc".format(fields[0])
        print(outpf_cc[0], outp)
        #delete if exists
        if os.path.exists(outp):
            os.remove(outp)
        #rename
        os.rename(outpf_cc[0], outp)
