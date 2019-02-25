#!/bin/bash
# 
# Bulk convert georeferenced images into geotif
# tif files are stored in the same folder as source
# existing files are not overwritten
#
for i in $*
do
	dest="${i%.*}.tif"	# remove extension from source filename & add tif
	if [ -e $dest ]
	then
		echo "Destination file $dest exists, skipped"
	else
		gdal_translate $i $dest
	fi
done
