#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
    Equalize images to the histogram of a reference image
    Based on 
"""
import argparse
import os
import sys
from skimage import exposure
import cv2
# command line parameters
parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
    help='pathes image files to process')
parser.add_argument("-r", "--reference", required=True,
	help="path to the input reference image")
parser.add_argument('--nowrite', action="store_true",
    help='show images')
parser.add_argument('--debug', action="store_true",
    help='show images')
args = parser.parse_args()
if not args.names:
    print("No input images given")
    parser.print_help()
    sys.exit(0)
# load the reference images
if args.debug:
    print("Loading reference image...")
ref = cv2.imread(args.reference)
# determine if we are performing multichannel histogram matching
multi = ref.shape[-1] > 1
for fn in args.names:
    if args.debug:
        print("Performing histogram matching for {}...".format(fn))
    src = cv2.imread(fn)
    matched = exposure.match_histograms(src, ref, multichannel=multi)
    if not args.nowrite:
        spl = os.path.splitext(fn)
        mn = spl[0] + "_matched" + spl[1]
        if args.debug:
            print("Writing matched image...")
        cv2.imwrite(mn, matched)
    if args.debug:
        # show the output images
        cv2.imshow("Source", src)
        cv2.imshow("Reference", ref)
        cv2.imshow("Matched", matched)
        cv2.waitKey(0)
