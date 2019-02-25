function nmea2deg(w) {
# conversion from NMEA agle to decimal degrees
    p = index(w, ".");
    return substr(w, 1, p-3) + substr(w, p-2, length(w)) / 60.0;
}

BEGIN { FS="[,]"; # field separator
    minlat = 90; minlon = 180;
    maxlat = -90; maxlon = -180;
}

{   token[$1]++;    # count different nmea sentences
    if ($1 == "\$GPGGA" && $7 == 1) {
        # convert angle to decimal degrees if fix
        lat = nmea2deg($3);
        if ($4 == "S") {
            lat = -lat;
        }
        lon = nmea2deg($5);
        if ($6 == "W") {
            lon = 360 - lon;
        }
        height = $10;
        # actualize min/max
        if (lat < minlat) { minlat = lat }
        if (lon < minlon) { minlon = lon }
        if (lat > maxlat) { maxlat = lat }
        if (lon > maxlon) { maxlon = lon }
    }
}

END {
    # print results
    print minlat, minlon, maxlat, maxlon
    for (i in token) {
        print i, token[i]
    }
}
