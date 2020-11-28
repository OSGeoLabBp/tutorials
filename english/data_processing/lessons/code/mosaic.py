#!/usr/bin/env python3
"""
    Cut image into mosaic rows and columns with one pixel overlap
"""
import sys
from osgeo import gdal

if len(sys.argv) < 2:
    print("Usage: {} image_file rows cols".format(sys.argv[0]))
    print(" rows and cols are optional default value is 4 for both")
    sys.exit(0)
DS = gdal.Open(sys.argv[1]) # load input dataset
if DS is None:
    print("Input dataset not found or not readable")
    sys.exit(1)
WIDTH = DS.RasterXSize      # get image size
HEIGHT = DS.RasterYSize
ROWS = COLS = 4
if len(sys.argv) > 2:           # get number of mosaic rows from command line
    ROWS = int(sys.argv[2])
if len(sys.argv) > 3:           # get number of mosaic cols from command line
    COLS = int(sys.argv[3])
ROW_STEP = int(HEIGHT / ROWS)   # row height
ROW_STEP1 = ROW_STEP + 1        # one pixel overlap between rows
COL_STEP = int(WIDTH / COLS)    # col width
COL_STEP1 = COL_STEP + 1        # one pixel overlap between rows
for j in range(0, WIDTH - COL_STEP + 1, COL_STEP):
    for i in range(0, HEIGHT - ROW_STEP + 1, ROW_STEP):
        name = "mosaic_{}_{}.tif".format(j, i)
        options = "-srcwin {} {} {} {}".format(j, i, COL_STEP1, ROW_STEP1)
        gdal.Translate(name, DS, options=options)
