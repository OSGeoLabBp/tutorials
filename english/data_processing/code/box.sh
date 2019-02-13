#! /bin/bash
if [ $# -ne 1 ]
then
	echo "usage? $0 <file>"
	exit 1
fi
if [ ! -f $1 ]
then
	echo "$1 file not found"
	exit 2
fi
for i in {1..3}
do
	./minmax.awk -F, -v col=$i $1
done
