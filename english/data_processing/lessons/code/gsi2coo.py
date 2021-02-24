#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Convert coordinates from Leica GSI16 file to CSV in metres
"""

import re
from sys import argv

# constants for units to meter in GSI
#     mm     1/1000ft   gon    DEG    DMS    mil  1/10 mm 1/10000ft     1/100mm
u = [1000, 1000 * 3.28, 'N/A', 'N/A', 'N/A', 'N/A', 10000, 10000 * 3.28, 100000]

def gsi_line(line):
    """ split GSI line into fields """
    fields = []
    i = 1
    while i < len(line):
        fields.append(line[i:i+23])
        i += 24
    return fields

def gsi_coo(fields):
    """ get coordis from fields of a GSI line """
    coords = {}             # initilize coordinates
    coords[0] = re.sub('^0+', '', fields[0][7:])  # point id always first
    for field in fields[1:]:
        if re.match('8[123]', field):   # or re.search('^8[123]', field)
            i = int(field[1])           # 1/2/3 Y/X/Z
            coords[i] = gsi_field(field)    # the coordinate
    return coords

def gsi_field(field):
    """ get field value im metres """
    s = 1 if field[6] == "+" else -1  # sign of coord
    d = u[int(field[5])]        # factor to metres
    w = int(field[7:])          # value in field
    return s * w / d            # value in metres with sign

if __name__ == "__main__":
    with open(argv[1], 'r') as fp:
        for line in fp:
            coords = gsi_coo(gsi_line(line.strip('\n')))
            if len(coords) == 4:    # 3D data found
                print("{} {:.3f} {:.3f} {:.3f}".format(coords[0], coords[1],
                    coords[2], coords[3]))
