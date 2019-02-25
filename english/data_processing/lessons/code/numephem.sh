#!/bin/bash
# process all files in current directory or files given by parameters
if [ $# -eq 0 ]
then
	# process all rinex file in current directory
	for file in brdm[0-3][0-9][0-9]0.[0-9][0-9]p
	do
		awk -f numephem.awk $file
	done
else
	# process rinex files given in the command line
	for file in "$@"
	do
		awk -f numephem.awk $file
	done
fi
