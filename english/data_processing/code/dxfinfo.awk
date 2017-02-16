#!/bin/gawk -f
# 
# statistics about entities and layers in a DXF file
# Zoltan Siki siki.zoltan@epito.bme.hu
# usage: dxfinfo.awk your_file.dxf
#		or
#        gawk -f dxfinfo.awk your_file.dxf > statistics.txt
#        gawk -f dxfinfo.awk your_file.dxf | sort > statistics.txt

BEGIN { # initialize variables
	last = ""; entity = ""; layer = "";
}
/ENTITIES/,/ENDSEC/ { # process only the entities section
	if (last == "  0") {	# last row entity start code?
		entity = $0;
	} else if (last == "  8") {	# last row layer name code?	
		layer = $0;
		dxf[layer,entity]++;	# increment entity count for layer, entity combination
	}
	last = $0;	# remember last input row
}
END {	# print out result
	for (i in dxf) {	# for each layer,entity pairs
		split(i, w, SUBSEP);	# separate layer and entity in index into w array
		print w[1], w[2], dxf[i];	# print layer, entity and count
	}
}
