/^[GREC][0-9][0-9]/ {
	# increment satelite specific array elements 
	# G - GPS, R - Glonass, E - Galielo, C - Beidou
	numsat[substr($0, 1, 1)]++;
}
END { printf "%s: ", FILENAME;
	name["G"] = "GPS"; name["R"] = "Glonass"; name["E"] = "Galileo";
	name["C"] = "Beidou";
	for (i in numsat) { printf "%s %d ", name[i], numsat[i]};
	printf "\n";
}
