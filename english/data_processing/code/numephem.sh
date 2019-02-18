#!/bin/bash

for file in "brdm"[0-3][0-9][0-9]"0."[0-9][0-9]"p"
do
	awk -f numephem.awk $file
done
