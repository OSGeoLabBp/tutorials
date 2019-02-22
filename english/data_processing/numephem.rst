Download and process RINEX navigation files
===========================================

*Keywords*: RINEX, broadcast ephemeris, download from command line

*Data files*: 

*Program files*: get_nav.sh, numephem.awk, numephem.sh

Download daily RINEX navigation files in version 3 for a specific period.
Then count the number of ephemerides broadcasted by different satellite systems, like GPS, Glonass, Galileo, Beidou...

download data (*get_nav.sh*)
----------------------------

.. code:: bash

	#!/bin/bash
	host="ftp://ftp.cddis.eosdis.nasa.gov/pub/gps/data/campaign/mgex/daily/rinex3/"
	if [ "$#" -ne 3 ]	#three arguments are obligatory to give
	then
		echo "usage $0 <year> <doy1> <doy2>"
		exit 1
	fi
	#the first argument is the year
	year=$1
	#the second one is the first day of year in the period
	doy1=$2
	#the third one is the last day of year in the period
	doy2=$3
	#get the last two characters of the year
	year2=${year:(-2)}
	#loop over the days of the period
	for (( i=$doy1; i<=$doy2; i++ ))
	do
		printf -v doy "%03d" $i	#format for having always three characters and leading zeros
		wget -N $host$year"/"$doy"/"$year2"p/brdm"$doy"0."$year2"p.Z"	#download
		uncompress "brdm"$doy"0."$year2"p"	#uncompress
	done
	
count ephemeris (*numephem.awk*)
--------------------------------

The basic idea is that a new ephemeris starts by a letter, abbreviation of the satellite system which is followed by two characters to identify the specific satellite. The letter 'G' corresponds to GPS (=NAVSTAR), R to Glonass, E to Galielo and C to Beidou. e.g. G01 means the 01 GPS satellite. Hence we have to count just the lines starts by the system id plus two integer numbers.

.. code:: awk

	/^[GREC][0-9][0-9]/ {
		# increment satelite specific array elements
		# G - GPS, R - Glonass, E - Galielo, C - Beidou
		numsat[substr($0, 1, 1)]++;
	}
	END { printf "%s: ", FILENAME;
		name["G"] = "GPS"; name["R"] = "Glonass"; name["E"] = "Galileo";
		name["C"] = "Beidou";
		for (i in numsat) { printf "%s %d ", name[i], numsat[i]};
		printf "\n";
	}

process navigation files (*numephem.sh*)
----------------------------------------

Loop over all files in the current directory with RINEX naming conventions 
if no command line parameters are given or process files given in the command 
line.

.. code:: bash

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

examples
--------

Download RINEX navigation files the first 5 days in 2019

.. code:: bash

	./get_nav.sh 2019 1 5
	
Count the ephemerides of the different satellite systems

.. code:: bash

	./numephem.sh

And the results:

.. code:: bash

	brdm0010.19p: Beidou 750 Galileo 4637 Glonass 1191 GPS 402 
	brdm0020.19p: Beidou 733 Galileo 4671 Glonass 1185 GPS 394 
	brdm0030.19p: Beidou 739 Galileo 4720 Glonass 1170 GPS 390 
	brdm0040.19p: Beidou 733 Galileo 4457 Glonass 1207 GPS 391 
	brdm0050.19p: Beidou 731 Galileo 4654 Glonass 1217 GPS 397 

*Development tipps*:

Improve *get_nav.sh* to handle invalid command line parameters and
if doy2 is not given download a single day (doy1).


