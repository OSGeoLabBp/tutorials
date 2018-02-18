#!/bin/bash
s=0
for i in `seq 1 10`; do
	let s=$s+$i         # `expr $s + $i`  or  $(($s+$i))  is the same
done
echo $s
