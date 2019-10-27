""" NMEA statistics
"""

import sys
import re

def checksum(buf):
    """ check nmea checksum on line """
    cs = ord(buf[1])
    for ch in buf[2:-3]:
        cs ^= ord(ch)
    return cs

def nmea2deg(nmea):
    """ convert nmea angle (dddmm.ss) to degree """
    w = nmea.rstrip('0').split('.')
    return int(w[0][:-2]) + int(w[0][-2:]) / 60.0 + int(w[1]) / 3600.0
    
fin = 'nmea2.txt'
if len(sys.argv) > 1:
    fin = sys.argv[1]   # get input file from command line
fi = open(fin, 'r') # input file
token = {}
minlat = 90
minlon = 180
maxlat = -90
maxlon = -180
for line in fi:
    line = line.strip()
    if hex(checksum(line))[2:].upper() != line[-2:]:
        print("Chechsum error: " + line)
        continue
    nmea = line.split(',')
    if nmea[0] not in token:
        token[nmea[0]] = 0
    token[nmea[0]] += 1
    if re.match('\$..GGA', line):
        if nmea[6] == '1':  # use only fix
            lat = nmea2deg(nmea[2])
            if nmea[3].upper() == 'S':
                lat *= -1
            lon = nmea2deg(nmea[4])
            if nmea[5].upper() == 'W':
                lon = 360 - lon
            height = float(nmea[9])
            if lat < minlat:
                minlat = lat
            if lon < minlon:
                minlon = lon
            if lat > maxlat:
                maxlat = lat
            if lon > maxlon:
                maxlon = lon
fi.close()
print (minlat, minlon, maxlat, maxlon)
for t in token:
    print("{}: {}".format(t, token[t]))
