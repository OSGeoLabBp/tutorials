#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Graph from monitoring data
    Command line parameters 
        1st csv input file
        2nd column number for point IDs (zero based, optional)
        3rd column number for x (datetime) values (optional)
        4th column number for y values (optional)
        5th point number to use in chart (optional) several point IDs can be given
            if no point IDs are given all points are plotted
"""

import sys
import numpy as np
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt    

if len(sys.argv) < 2:
    print("""
usage: input_csv_file p_num_col x_colum y_column [p_num1 [pnum2 ...]]
    Command line parameters 
        1st csv input file
        2nd column number for point IDs (zero based)
        3rd column number for x (datetime) values
        4th column number for y values
        5th point number to use in chart (optional) several point IDs can be given
            if no point IDs are given all points are plotted
        """)
    sys.exit()

if not os.path.exists(sys.argv[1]):
    print("File does not exist: " + sys.argv[1])
    sys.exit()
p_col = 0       # column number for point numbers values
if len(sys.argv) > 2:
    p_col = int(sys.argv[2])
x_col = 4       # column for x values
if len(sys.argv) > 3:
    x_col = int(sys.argv[3])
y_col = 3       # column for y values
if len(sys.argv) > 4:
    y_col = int(sys.argv[4])
p_nums = None
if len(sys.argv) > 5:
    p_nums = sys.argv[4:]
# load data into dict for point numbers
data = {}
with open(sys.argv[1], newline='') as f:
    for row in csv.reader(f, delimiter=";"):
        p_num = row[p_col]
        if p_nums is not None and p_num not in p_nums:
            continue    # skip point
        dt = datetime.strptime(row[x_col], "%Y-%m-%d %H:%M:%S")
        y = float(row[y_col])
        if not p_num in data:
            data[p_num] = [[], []]
        data[p_num][0].append(dt)
        data[p_num][1].append(y)
fig = plt.figure(1)
for key, val in data.items():
    plt.plot_date(val[0], val[1], '-', label=key)
#for key in data.keys():
#    plt.plot_date(data[key][0], data[key][1], '-', label=key)
plt.xticks(rotation=45)
plt.xlabel("date time")
plt.grid()
plt.legend()
plt.show()
