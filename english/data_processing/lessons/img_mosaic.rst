Create image mosaic
===================

*Keywords:* bash, gdal, imagemagic, python

*Program files:* mosaic.sh, mosaic.py

Let's imagine we have a large orthophoto image created from UAV images
(~500 MB compressed jpeg image file). If you used it in QGIS on
an average computer, zoom in/out would be slow. We will cut the image into
uncompressed tiles to make the rendering faster when zooming in.

GDAL utilities will be used from bash script and python. We shall create tiles with one
pixel overlap to avoid white lines between the mosaic items because of rounding 
errors. The script queries the size of the image and divides it pieces.
The number of rows and columns can be given from the command line.

The bash script uses image magic to get image size (*identify*).
Here is the bash script:

.. code:: bash

    #!/bin/bash
    if [ $# -lt 1 ]
    then
        echo Usage: $0 image_file rows cols
        exit 1
    fi
    WIDTH=`identify -quiet -format '%w' $1`     # get image width
    HEIGHT=`identify -quiet -format '%h' $1`    # get image height
    ROWS=4                                      # default number or rows
    COLS=4                                      # default number of columns
    if [ $# -gt 1 ]
    then
        ROWS=$2                         # get number of rows from command line
    fi
    if [ $# -gt 2 ]
    then
        COLS=$3                         # get number of columns from command line
    fi
    ROWSTEP=$( expr $HEIGHT / $ROWS )
    ROWSTEP1=$( expr $ROWSTEP + 1 )
    COLSTEP=$( expr $WIDTH / $COLS )
    COLSTEP1=$( expr $COLSTEP + 1)
    for ((j=0;j<=$WIDTH-$COLSTEP;j+=$COLSTEP))
    do
        for ((i=0;i<=$HEIGHT-$ROWSTEP;i+=$ROWSTEP))
        do
            gdal_translate -srcwin $j $i $COLSTEP1 $ROWSTEP1 $1 mosaic_${j}_${i}.tif
        done
    done

The Python script uses only *gdal* Python package and loads the input image
into memory at the beginning. 

.. code:: python

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
    WIDTH = DS.RasterXSize          # get image size
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

After running one of the scripts on a georeferenced image, we get mosaic_n_m.tif files
where *n* and *m* are the upper left corner pixel positions of the mosaic in
the original image.
Depending on the used hardware 50-300MB mosaic parts can be optimal.

I tested the performance of the two scripts with a georeferenced jpg file with 22747 x 18185 pixels.
The increasing run time difference is caused by the loading of input image for each mosaic in case of bash script.

+---------+------------+--------------+
| mosaic  | bash       | Python       |
+---------+------------+--------------+
| 2 x 2   |   8 sec    |  6 sec       |
+---------+------------+--------------+
| 4 x 4   |  24 sec    | 10 sec       |
+---------+------------+--------------+
| 8 x 8   |  90 sec    | 18 sec       |
+---------+------------+--------------+
| 16 x 16 | 330 sec    | 39 sec       |
+---------+------------+--------------+

Having several images instead of one is not comfortable. Using *gdalbuildvrt*
command a virtual raster can be created.

.. code::

    gdalbuildvrt mosaic.vrt ./mosaic*.tif

Virtual rasters are supported by several GIS programs (e.g. QGIS, MapServer,
GDAL). To improve the preformance more, pyramids can be created for the
individual tif files using *gdaladdo*.

.. code::

    for i in ./mosaic*.tif; do gdaladdo -ro -r cubic $i 2 4 8; done

The command above creates .ovr files (external overviews).

If you would like to publish ortophoto on the internet, the most effective 
solution is the XYZ tile format. XYZ tiles can be created using *gdal2tiles*, but 
tiles are transformed to web mercator CRS.

An extended version of mosaic.py is also avalilable called **mosaicplus.py**.
Not only the number of row and columns can be set, but an alternative 
solution available to set the size of mosaic tiles in pixels. If both are
given tile width and height are considered. A new extent for the output can
also be set from 
the command line with coordinates in the used coordinate reference system (CRS).
All the command line parameters are considered for one or more images given 
also in the command line.

.. code::

    usage: mosaicplus.py [-h] [--rows ROWS] [--cols COLS] [--width WIDTH]
                         [--height HEIGHT] [--minx MINX] [--miny MINY]
                         [--maxx MAXX] [--maxy MAXY] [--over OVER] [--extend]
                         [file_names [file_names ...]]

    positional arguments:
      file_names       image files to process

    optional arguments:
      -h, --help       show this help message and exit
      --rows ROWS      number of mosaic rows, default 4
      --cols COLS      number of mosaic cols, default 4
      --width WIDTH    width of mosaic tiles
      --height HEIGHT  height of mosaic tiles
      --minx MINX      minimal x coordinate of extent to clip from image
      --miny MINY      minimal y coordinate of extent to clip from image
      --maxx MAXX      maximal x coordinate of extent to clip from image
      --maxy MAXY      maximal y coordinate of extent to clip from image
      --over OVER      overlap between rows and columns in pixels, default 1
      --extend         create last pairtial row and column, too

.. note::

    *Development tipps:*
    Extend the scripts to create virtual raster and overviews, too.
