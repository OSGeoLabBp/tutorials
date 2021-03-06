Bulk image convert to GeoTiff
=============================

*Keywords:* bash, gdal, GeoTiff

*Program file:* img2tif.sh, img2tif.py

Our aim is to convert different georeferenced image files (e.g. .png & .pgw)
into a single georeferenced tiff file. GDAL utilities and Python will be used.

GDAL utilities
--------------

GDAL utilities (http://www.gdal.org/gdal_utilities.html) are CLI programs which
can be used from scripts. gdal_translate will be used from the rich set
of GDAL utilities. gdal_translate can convert between different image 
formats, cut part of image, reduce resolution, etc.
The default output format of all GDAL utility programs is the GeoTiff.

Writing the script
------------------

gdal_translate can process a single file, so a bash script will be written
to convert several files. The following exxample converts the png file into
GeoTiff, which is the default output format of GDAL utilities.

.. code:: bash

	gdal_translate sample.png sample.tif

Let's add a loop to our command to convert more files.

.. code:: bash

	for i in $*
	do
		dest="${i%.*}.tif"  # remove extension from source filename & add tif
		if [ -e $dest ]
		then
			echo "Destination file $dest exists, skipped"
		else
			gdal_translate $i $dest
		fi
	done

.. note::

	To get the file name and extesion without path use: *$(basename $i)*.
	To get the extension use: *${i##\*.}*.

.. note::

	If you would like change the resolution of the image too, use
	*-outsize xsize[%] ysize[%]* and *-r* for resampling method.
	The imgemagick *convert* commad can also be used to resize images,
	but that won't preserve georeference.

Python solution (img2tif.py)

.. code:: Python

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
