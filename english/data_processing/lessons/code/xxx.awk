/^[GREC][0-9][0-9]/ { i = substr($0, 1, 1); numsat[i]++; }
END { print FILENAME;
	for (i in numsat) { print i, numsat[i]} }
