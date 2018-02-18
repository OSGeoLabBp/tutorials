#!/bin/bash
s=0
for i in `seq 1 $1`; do
	s=$(($s+$i))
done
echo $s

