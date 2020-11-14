Create image mosaic
===================

*Keywords:* bash, gdal, imagemagic

*Program file:* mosaic.sh

Let's imagine we have a large orthophoto image created from UAV images
(~500 MB compressed jpeg image file). If you used it in QGIS on
an average computer, zoom in/out would be slow. We will cut the image into
uncompressed tiles to make the rendering faster.

GDAL utilities will be used from bash script. We shall create tiles with one
pixel overlap avoid white lines between the mosaic items because of rounding 
errors. The script queries the size of the image and divides it pieces.
The number of rows and columns can be given from the command line.

Here is the script:

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

After runnuing the script on a georeferenced image, wee get mosaic_n_m.tif files
where n and m are the upper left corner pixel position of the mosaic.
Depending on the used hardware 50-300MB mosaic parts can be optimal.

Having several images instead of one is not comfortable. Using *gdalbuildvrt*
command a virtual raster can be created.

.. code::

    gdalbuild mosaic.vrt ./mosaic*.tif

Virtual rasters are supported by several GIS programs (e.g. QGIS, MapServer,
GDAL). To improve the preformance more, pyramids can be created for the
individual tif files using *gdaladdo*.

.. code::

    for i in ./mosaic*.tif; do gdaladdo -ro -r cubic $i 2 4 8; done

The command above creates .ovr files (overviews).

If you would like to publish ortophoto on the internet, the most effective 
solution is the XYZ tile. XYZ tiles can be created using *gdal2tiles*, but 
tiles are created in web mercator CRS.

.. note::

    *Development tipps:*
    Write Python program using GDAL Python bindings to make image mosaic.
