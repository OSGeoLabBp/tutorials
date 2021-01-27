#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Read GSI 16 file and write coordinates in metres to standard output
"""

import re
from sys import argv

# unit multiplyers
u = [1000, 1000 * 3.28, 10000, 10000 * 3.28, 100000]

with open(argv[1], 'r') as fp:
    for line in fp:
        if line.startswith("*"):
            coords = {}
            fields = line.split()                       # space separated fields
            pid = re.sub('^0+', '', fields[0][9:])      # point id
            for field in fields[1:]:
                if re.match('8[123]', field):
                    index = int(field[1])               # 1/2/3 e/n/z
                    s = 1 if field[6] == "+" else -1    # sign for coord
                    d = u[int(field[5])]                 # divider for units
                    w = int(field[7:])
                    coords[index] = s * w / d
            print("{} {:.3f} {:.3f} {:.3f}".format(pid, coords[1], coords[2], coords[3]))
