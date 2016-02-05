# function to convert angles from dddmm.mmmm to decimal degrees
function nmea2deg(w) {
    p = index(w, ".");
    return substr(w, 1, p-3) + substr(w, p-2, length(w)) / 60.0;
}
BEGIN { FS="[,]"; }     # set field separator
/^\$GPGGA,/ {
    if ($7 == 1) {      # fix position?
        lat = nmea2deg($3);
        if ($4 == "S") {
            lat = -lat;
        }
        lon = nmea2deg($5);
        if ($6 == "W") {
            lon = 360 - lon;
        }
        height = $10;
        print lat, lon, height;
    }
}
