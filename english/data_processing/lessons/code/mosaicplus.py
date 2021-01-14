#!/usr/bin/env python3
"""
    Cut image into mosaic rows and columns with one pixel overlap
"""
import sys
import argparse
import os
import tempfile
from osgeo import gdal

parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
                    help='image files to process')
parser.add_argument('--rows', type=int, default=4,
                    help='number of mosaic rows, default 4')
parser.add_argument('--cols', type=int, default=4,
                    help='number of mosaic cols, default 4')
parser.add_argument('--width', type=int,
                    help='width of mosaic tiles')
parser.add_argument('--height', type=int,
                    help='height of mosaic tiles')
parser.add_argument('--minx', type=float,
                    help='minimal x coordinate of extent to clip from image')
parser.add_argument('--miny', type=float,
                    help='minimal y coordinate of extent to clip from image')
parser.add_argument('--maxx', type=float,
                    help='maximal x coordinate of extent to clip from image')
parser.add_argument('--maxy', type=float,
                    help='maximal y coordinate of extent to clip from image')
parser.add_argument('--over', type=int, default=1,
                    help='overlap between rows and columns in pixels, default 1')
parser.add_argument('--extend', action="store_true",
                    help='create last patial row and column')

args = parser.parse_args()
if not args.names:
    print("no input image(s) given")
    parser.print_help()
    sys.exit(0)
if args.width and args.height:
    ROW_STEP = int(args.width)
    COL_STEP = int(args.height)
    ROWS = COLS = None
else:
    ROWS = int(args.rows)
    COLS = int(args.cols)
    ROW_STEP = COL_STEP = None

if args.minx and args.miny and args.maxx and args.maxy:
    CLIP_MINX = float(args.minx)
    CLIP_MINY = float(args.miny)
    CLIP_MAXX = float(args.maxx)
    CLIP_MAXY = float(args.maxy)
else:
    CLIP_MINX = CLIP_MINY = CLIP_MAXX = CLIP_MAXY = None

PIXEL_OVER = int(args.over)
for name in args.names:
    DS = gdal.Open(name) # load input dataset
    if DS is None:
        print("Input dataset not found or not readable")
        continue
    if CLIP_MINX is not None:
        TEMP_NAME = tempfile.mktemp() + '.tif'
        DS = gdal.Translate(TEMP_NAME, DS, projWin=[CLIP_MINX, CLIP_MAXY, CLIP_MAXX, CLIP_MINY])
        os.remove(TEMP_NAME)
    WIDTH = DS.RasterXSize      # get image size
    HEIGHT = DS.RasterYSize
    if args.width is None:
        ROW_STEP = int(HEIGHT / ROWS)   # row height
        COL_STEP = int(WIDTH / COLS)    # col width
    else:
        i, j = divmod(HEIGHT, ROW_STEP)
        ROWS = i if j == 0 else i + 1
        i, j = divmod(WIDTH, COL_STEP)
        COLS = i if j == 0 else i + 1
    ROW_STEP1 = ROW_STEP + PIXEL_OVER   # some pixel overlap between rows
    COL_STEP1 = COL_STEP + PIXEL_OVER   # some pixel overlap between rows
    OUT, _ = os.path.splitext(name)
    MAXJ = WIDTH - PIXEL_OVER if args.extend else WIDTH - COL_STEP + 1
    MAXI = HEIGHT - PIXEL_OVER if args.extend else WIDTH - COL_STEP + 1
    for j in range(0, MAXJ, COL_STEP):
        for i in range(0, MAXI, ROW_STEP):
            name = "{}_{}_{}.tif".format(OUT, j, i)
            options = "-srcwin {} {} {} {}".format(j, i, COL_STEP1, ROW_STEP1)
            gdal.Translate(name, DS, options=options)
