#!/bin/bash
if [ $# -lt 1 ]; then
	echo Invalid number of parameters
	echo usage: sum2.sh n1 n2 ...
	exit 1
fi
for j in $*; do
	s=0
	for i in `seq 1 $j`; do
		s=$(($s+$i))
	done
	echo $s
done

