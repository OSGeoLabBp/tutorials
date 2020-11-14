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
