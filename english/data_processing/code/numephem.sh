#!/bin/bash
# process all files in current directory or files given by parameters
if [ $# -eq 0 ]
then
	for file in brdm[0-3][0-9][0-9]0.[0-9][0-9]p
	do
		awk -f numephem.awk $file
	done
else
	for file in "$@"
	do
		awk -f numephem.awk $file
	done
fi
