#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter ascii point cloud save every nth line optionally with row number
    output is sent to standard output use > to save it to file
    usage: python filter_n.py <switches> [input1 input2 input3]
        switches:
            -i or --input_separator separator in input file, default ","
            -o or --output_separator separator in output file, default ","
            -r or --rows keep only every rth rows, default 1, all lines
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
        i_fp (file) - handle to input file
    """
    i = j = 0   # initialize input and output row numbers
    # set up format for required decimals
    for line in i_fp:
        i += 1          # count input lines
        if i % r_skip == 0:  # write only every rth line
            j += 1      # count output lines
            items = line.split(i_sep)
            n_items = len(items)
            if n_items in (3, 4):
                try:
                    # convert coordinate fields to numbers for formatting
                    x_coo, y_coo, z_coo = [float(c) for c in items[-3:]]
                except ValueError:
                    continue    # spkip invalid line
                line_no = str(j) + o_sep if row_num else ''
                if n_items == 3: # no point id
                    print(f"{line_no}{x_coo:.{n_dec}f}{o_sep}{y_coo:.{n_dec}f}{o_sep}{z_coo:.{n_dec}f}")
                else:
                    print(f"{line_no}{items[0]}{o_sep}{x_coo:.{n_dec}f}{o_sep}{y_coo:.{n_dec}f}{o_sep}{z_coo:.{n_dec}f}")

parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
                    help='files to process')
parser.add_argument('-i', '--input_separator', type=str, default=',',
                    help='input separator, default ","')
parser.add_argument('-o', '--output_separator', type=str, default=',',
                    help='output separator, default ","')
parser.add_argument('-r', '--rows', type=int, default=1,
                    help='rows to keep, default 1')
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
    except Exception:
        continue        # skip files not found
    pc_filter(args.nums, args.rows, args.decimals, args.input_separator,
              args.output_separator, fp)
