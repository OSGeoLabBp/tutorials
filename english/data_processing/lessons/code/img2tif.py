#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    convert input gereferenced images to geotif
    usage: python img2tif sample.png
           python img2tif *.jpg 
"""
import sys
from os import path
from osgeo import gdal

for inName in sys.argv[1:]:             # go through input files
    outName = path.splitext(inName)[0] + '.tif'
    if path.exists(outName):
        print("{} file exists, skipped".format(outName))
    src = gdal.Open(inName)
    dst = gdal.Warp(outName, src)
    dst = None
