# -*- coding: utf-8 -*-
"""
    Parse Nikon recorded observations

    Nikon total stations save observations into variable length and variable structure delimited text file.

    Sample from the file:

    CO,HA Raw data: Azimuth
    CO,Tilt Correction:  VA:OFF HA:OFF
    CO, TOPO <JOB> Created 01-Jan-2001 05:00:27
    MP,OMZ1,,4950153.530,5173524.258,341.532,
    MP,OMZ2,,4950392.611,5173092.830,306.781,
    CO,Temp:30C Press:740mmHg Prism:0 01-Jan-2001 05:39:35
    ST,OMZ1,,OMZ2,,0.000,298.5937,298.5937
    F1,OMZ2,0.000,494.429,0.0000,94.0142,05:39:35
    SS,1,0.000,111.109,268.2305,101.4007,05:46:01,

    The first two characters in each line mark the type of the record.
"""

from sys import argv
from math import pi
ro = 180 / pi * 3600          # one radian in seconds

def to_rad(pseudo_dms):
    """ convert pseudo DMS string (DDD.MMSS) to radians """
    w = pseudo_dms.split('.')     # separate degree and MMSS
    degree = int(w[0])
    minute = int(w[1][:2])
    second = int(w[1][2:])
    return (degree + minute / 60 + second / 3600) / 180 * pi

def to_dms(angle):
    """ convert angle from radian to DMS string """
    s = int(angle * ro)
    degree, s = divmod(s, 3600)
    minute, s = divmod(s, 60)
    return f'{degree:d}-{int(minute):02d}-{int(s):02d}'

if len(argv) < 2:
    print("Please specify an input file in the command line")
    exit(-1)
field_book = []                                   # list to store field-book data
with open(argv[1]) as f:
    for line in f:                                  # process file line by line
        rec_list = line.strip('\n\r').split(',')      # remove EOL marker(s) and slip by comma
        rec_dict = {}                                 # empty dictionary for needed data
        if rec_list[0] == 'ST':                       # station record
            rec_dict['station'] = rec_list[1]           # station id
            rec_dict['ih'] = float(rec_list[5])         # instrument height
            field_book.append(rec_dict)
        elif rec_list[0] in ('F1', 'SS'):               # observation in face left
            rec_dict['target'] = rec_list[1]            # target id
            rec_dict['th'] = float(rec_list[2])         # target height
            rec_dict['sd'] = float(rec_list[3])         # slope distance
            rec_dict['ha'] = to_rad(rec_list[4])        # mean direction
            rec_dict['za'] = to_rad(rec_list[5])        # zenith angle
            if len(rec_list) > 7 and len(rec_list[7]) > 0:
                rec_dict['cd'] = rec_list[7]              # point code
            else:
                rec_dict['cd'] = ''
            field_book.append(rec_dict)

header1 = '----------------------------------------------------------'
header2 = '| station| target |  HA     |  VA     |    SD   |  Code  |'
print(header1)
print(header2)
print(header1)
for rec in field_book:
    if 'station' in rec:
        print(f"|{rec['station']:8s}|        |         |         |         |        |")
    elif 'target' in rec:
        print(f"|        |{rec['target']:8s}|{to_dms(rec['ha']):>9s}|{to_dms(rec['za']):>9s}|{rec['sd']:9.3f}|{rec['cd']:8s}|")
print(header1)
