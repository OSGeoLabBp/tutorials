BEGIN {
	print "EAST;NORTH;LAYER;DIRECTION;SIZE;TEXT";	# print header
}
/^ENTITIES/,/^EOF/ {
	if ($0 == "  0") {					# next entity reached
		if (entity == "TEXT") {			# output text data
			printf("%.2f;%.2f;%s;%.5f;%.2f;%s\n", x, y, layer, angle, size, txt);
		}
		entity = ""; txt = ""; angle = 0; size = 1; layer = "";
		last = "";						# initialize variables
	}
	if (last == "  0") { entity = $0; }	# actual entity type
	if (last == "  8") { layer = $0; }	# layer
	if (last == " 10") { x = $0; }		# east	
	if (last == " 20") { y = $0; }		# north
	if (last == " 40") { size = $0; }	# text size
	if (last == " 50") { angle = $0; }	# text direction
	if (last == "  1") { txt = $0; }	# text
	last = $0;							# last input line
}
