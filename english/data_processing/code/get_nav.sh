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
	rm "brdm"$doy"0."$year2"p" "brdm"$doy"0."$year2"p.Z" # remove previous
	wget -N $host$year"/"$doy"/"$year2"p/brdm"$doy"0."$year2"p.Z"	#download
	uncompress "brdm"$doy"0."$year2"p"	#uncompress
done
