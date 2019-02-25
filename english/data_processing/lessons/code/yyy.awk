/^[GREC][0-9][0-9]/ { numsat[substr($0, 1, 1)]++; }
END { printf "%s: ", FILENAME;
	for (i in numsat) { printf "%c %d ", i, numsat[i]};
	printf "\n";
}
