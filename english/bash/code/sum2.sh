#!/bin/bash
if [ $# -ne 1 ]; then
	echo Invalid number of parameters
	echo usage: sum2.sh n
	exit 1
fi
s=0
for i in `seq 1 $1`; do
	s=$(($s+$i))
done
echo $s

