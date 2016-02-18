BEGIN {
	FS = "[\|]";	# field separator
}

/\|Y / {			# y coordinate given in thi line
	y = x = z = 0;
	for (i = 1; i <= NF; i++) {			# check all fields
		if (match($i, /^PI1[ \t]+/)) {	# point id
			id = substr($i, 20);		# skip first 20  chars
			sub(/^ +/, "", id);			# remove leading spaces
		} else if (match($i, /^Y[ \t]+/)) {	# y coordinate
			y = substr($i, 2);			# skip first character
			sub(/^ +/, "", y);			# remove leading spaces
			sub(/ m +$/, "", y);		# remove trailing spaces and dimension
		} else if (match($i, /^X[ \t]+/)) { # x coordinate
			x = substr($i, 2);			# skip first character
			sub(/^ +/, "", x);			# remove leading spaces
			sub(/ m +$/, "", x);		# remove trailing spaces and dimension
		} else if (match($i, /^Z[ \t]+/)) {	# z coordinate
			z = substr($i, 2);			# skip first character
			sub(/^ +/, "", z);			# remove leading spaces
			sub(/ m +$/, "", z);		# remove trailing spaces and dimension
		}
	}
	print id, y, x, z;	# print coordinates
}
