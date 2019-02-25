#!/bin/bash
for i in $*
do
	identify -format '%[EXIF:GPS*]' $i | gawk -v fn="$i" -f exif.awk
done
