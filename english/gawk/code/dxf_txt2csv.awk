BEGIN {
	print "EAST;NORTH;LAYER;DIRECTION;SIZE;TEXT";	# print header
	rad2deg = 180.0 / atan2(1.0, 1.0) / 4;
}
/^ENTITIES/,/^EOF/ {
	if ($0 == "  0") {					# next entity reached
		if (entity == "MTEXT") {		# calculate angle from dx, dy
			angle = atan2(dy, dx) * rad2deg;	# angle in deg
		}
		if (entity == "TEXT" || entity == "MTEXT") {	# output text data
			printf("%.2f;%.2f;%s;%.5f;%.2f;%s\n", x, y, layer, angle, size, txt);
		}
		entity = ""; txt = ""; angle = 0; size = 1; layer = "";
		dx = dy = 0.0;
		last = "";						# initialize variables
	}
	if (last == "  0") { entity = $0; }	# actual entity type
	if (last == "  8") { layer = $0; }	# layer
	if (last == " 10") { x = $0; }		# east	
	if (last == " 20") { y = $0; }		# north
	if (last == " 11") { dx = $0; }		# direction for MTEXT	
	if (last == " 21") { dy = $0; }		# direction for MTEXT
	if (last == " 40") { size = $0; }	# text size
	if (last == " 50") { angle = $0; }	# text direction
	if (last == "  1") { txt = $0; }	# text
	last = $0;							# last input line
}
