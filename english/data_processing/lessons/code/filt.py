#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter ascii point cloud save every nth line optionally with row number
    output is sent to standard output use > to save it to file
    usage: python filter_n.py <switches> [input1 input2 input3]
        switches:
            -i or --input_separator separator in input file, default ","
            -o or --output_separator separator in output file, default ","
            -r or --rows keep only every rth rows, default 10
            -d or --decimals write d decimals to output, default 3
            -n or --nums add row numbers to output
        input - name of ascii point cloud or standard input if none given
"""
import sys          # for sys.stdin
import argparse     # for command line parameters processing

def pc_filter(row_num, r_skip, n_dec, i_sep, o_sep, i_fp):
    """ filter an ascii point cloud
        row_num (boolean) - add row numbers if true
        r_skip (int) - only every rth row is written to the output
        n_dec (int) - number of decimals in output
        i_sep (char) - input separator
        o_sep (char) - output separator
        i_fp (file) - hndle to input file
    """
    i = j = 0   # initialize input and output row numbers
    # set up format for required decimals
    form = "{2:." + str(n_dec) + "f}{0}{3:." + str(n_dec) + \
           "f}{0}{4:." + str(n_dec) + "f}"
    if row_num:   # add row number to format string
        form = "{1:d}{0}" + form
    for line in i_fp:
        i += 1          # count input lines
        if i % r_skip == 0:  # write only every rth line
            j += 1      # count output lines0
            # change input fields to numbers for formatting
            x_coo, y_coo, z_coo = [float(c) for c in line.split(i_sep)]
            print(form.format(o_sep, j, x_coo, y_coo, z_coo))

parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
                    help='files to process')
parser.add_argument('-i', '--input_separator', type=str, default=',',
                    help='input separator, default ","')
parser.add_argument('-o', '--output_separator', type=str, default=',',
                    help='output separator, default ","')
parser.add_argument('-r', '--rows', type=int, default=10,
                    help='rows to keep, default 10')
parser.add_argument('-d', '--decimals', type=int, default=3,
                    help='number of decimals in output co-ordinates, default 3')
parser.add_argument('-n', '--nums', action='store_true',
                    help='add row numbers to output, default off')
args = parser.parse_args()

if not args.names:  # process standard input
    pc_filter(args.nums, args.rows, args.decimals, args.input_separator,
              args.output_separator, sys.stdin)

for fn in args.names:   # process all files from commandline
    try:
        fp = open(fn)
    except:
        continue        # skip files is not found
    pc_filter(args.nums, args.rows, args.decimals, args.input_separator,
              args.output_separator, fp)
