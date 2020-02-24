Filter point cloud
==================

*keywords*: point cloud, command line parameters

*Data file*: lidar.txt

*Program files*: filter_n.py, filt.py

Let's write a program to to preserve only every nth point from an input point
cloud. The input text file contains coordinates (x, y, z) of a point in a line.

Sample lines from input text file:

.. code:: txt

	548025.89,5129282.50,1008.79
	548026.41,5129284.81,1009.49
	548026.81,5129270.56,1005.94
	548027.89,5129275.27,1007.15
	548029.48,5129282.28,1009.18
	548031.57,5129291.52,1011.97
	548032.78,5129290.76,1012.10

Simple solution in gawk
-----------------------

Our program is so short we can input it in the command line. It will write 
every 10th line to the output.

.. code:: awk

	gawk '{ if (NR % 10 == 0) {print $0;} }' lidar.txt > lidar_psz.txt

NR is a special gawk variable which holds the line number of the actually
processed line. The % operator returns the modulo of the division.

.. note::

	On windows you have to use double quote around the program code on the
	command line.

Python solution
---------------

In our first naive code (filter_n.py) takes the number of lines to skip and
the name of the input file from the command line and write filtered lines to
the standard output.
Every 10th line is written to the output if no number of lines to skip is given .
If no input file given it reads the standard input.

.. code:: python

	""" filter ascii point cloud save every nth line
		usage: python filter_n.py n [input}
			n - lines to written, default: 10
			input - name of ascii point cloud or standard input
	"""
	import sys

	i = 0
	n = 10
	if len(sys.argv) > 1:
		try:
			n = int(sys.argv[1])
		except:
			sys.exit(-1)
	if len(sys.argv) > 2:
		try:
			fp = open(sys.argv[2])
		except:
			sys.exit(-2)
	else:
		fp = sys.stdin
	for line in fp:
		i += 1
		if i % n == 0:
			print(line.strip())

Let's make our code more flexible. To create a more useful tool 

* change the precision in the output to defined number of decimals
* accept input and output separator
* optionally add row id to output

This means we have to use more and more command line options, the previous
positional approache is not acceptable. Let's use command line switches.
There is a standard module in Python for that purpose called *argparse*.
To tell you the truth, there is a module for nearly everything in Python.

Here is the code:

.. code:: python

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


.. note:: Development tips

	Extend the Python code to filter points in a 3D box

CloudCompare
------------

The open source CloudCompare can be a premium solution to solve point cloud
filtering. It has a command line interface, too, it supports several text and
binary data formats, it has more intelligent filtering (random, space, octree).
The next command reads silently the lidar.txt and uses octree method to reduce
the number of points and saves to a binary file.

.. code:: bash

	CloudCompare -SILENT -O lidar.txt -SS OCTREE 8 -AUTO_SAVE ON

You can read more about command line usage of CloudCompare `here <https://www.cloudcompare.org/doc/wiki/index.php?title=Command_line_mode>`_.
