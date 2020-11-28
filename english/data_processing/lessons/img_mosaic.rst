Create image mosaic
===================

*Keywords:* bash, gdal, imagemagic, python

*Program file:* mosaic.sh, mosaic.py

Let's imagine we have a large orthophoto image created from UAV images
(~500 MB compressed jpeg image file). If you used it in QGIS on
an average computer, zoom in/out would be slow. We will cut the image into
uncompressed tiles to make the rendering faster.

GDAL utilities will be used from bash script and python. We shall create tiles with one
pixel overlap to avoid white lines between the mosaic items because of rounding 
errors. The script queries the size of the image and divides it pieces.
The number of rows and columns can be given from the command line.

THe bash script uses image magic to get image size (identify).
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

The Python script uses only gdal PYthon package and loads the input image
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
where n and m are the upper left corner pixel position of the mosaic.
Depending on the used hardware 50-300MB mosaic parts can be optimal.

Having several images instead of one is not comfortable. Using *gdalbuildvrt*
command a virtual raster can be created.

.. code::

    gdalbuildvrt mosaic.vrt ./mosaic*.tif

Virtual rasters are supported by several GIS programs (e.g. QGIS, MapServer,
GDAL). To improve the preformance more, pyramids can be created for the
individual tif files using *gdaladdo*.

.. code::

    for i in ./mosaic*.tif; do gdaladdo -ro -r cubic $i 2 4 8; done

The command above creates .ovr files (overviews).

If you would like to publish ortophoto on the internet, the most effective 
solution is the XYZ tile. XYZ tiles can be created using *gdal2tiles*, but 
tiles are transformed to web mercator CRS.

.. note::

    *Development tipps:*
    Extend the scripts to create virtual raster and overview, too.
    Compare the speed of the two solutions.
