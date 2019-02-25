BEGIN { FS = "[=,/]"; }
/^exif:GPSDateStamp=/ { idate = $2; }
/^exif:GPSTimeStamp=/ { ihour = $2 / $3; imin = $4 / $5; isec = $6 / $7; }
/^exif:GPSLatitudeRef=/ { if ($2 == "N") { plat = ""; } else { plat = "-" } }
/^exif:GPSLongitudeRef=/ { if ($2 == "E") { plon = ""; } else { plon = "-" } }
/^exif:GPSLatitude=/ { lat = $2 / $3 + $4 / $5 / 60 + $6 / $7 / 3600; }
/^exif:GPSLongitude=/ { lon = $2 / $3 + $4 / $5 / 60 + $6 / $7 / 3600; }
END { printf "%s;%s%.6f;%s%.6f;%s %d:%d:%.1f\n",
		fn, plon, lon, plat, lat, idate, ihour, imin, isec; }
