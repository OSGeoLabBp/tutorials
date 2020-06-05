#! /usr/bin/env python3
"""
   Sample code to demonstrate effectiveness of algorithms
"""
import time
import sys
import os
import numpy as np

def num(an_array):
    """ number of rows in a numpy array """
    return an_array.size

ARGC = len(sys.argv)
if ARGC == 1:
    print("usage: {} point_file [step] [min/max/mean/median/num]\n".format(sys.argv[0]))
    sys.exit(1)
fname = sys.argv[1]
# grid sizes
DX = 0.1
if ARGC > 2:
    DX = float(sys.argv[2])
d = np.array([DX, DX, DX])
# function for interpolation
fu = np.amin
if ARGC > 3:
    if sys.argv[3][0:2].lower() == "mi":        # minimum Z
        fu = np.amin
    elif sys.argv[3][0:2].lower() == "ma":      # maximum Z
        fu = np.amax
    elif sys.argv[3][0:3].lower() == "mea":     # mean Z
        fu = np.mean
    elif sys.argv[3][0:3].lower() == "med":     # median Z
        fu = np.median
    elif sys.argv[3][0:2].lower() == "nu":      # number of points
        fu = num
no_data = -9999.0       # nodata in generated ascii grid

# load ascii point cloud x y z ...
start_time = time.time()
points = np.loadtxt(fname)
print("--- reading {} seconds ---".format((time.time() - start_time)))

start_time1 = time.time()
# delete extra columns
points = np.delete(points, np.s_[3:], axis=1)
# get extent
minp = np.amin(points, axis=0)
maxp = np.amax(points, axis=0)
# round to grid values
minp = np.floor(minp / d) * d
maxp = np.ceil(maxp / d) * d
# number of buckets along the axes
n = ((maxp - minp) / d).astype('int32')
# creating index bucket rows and columns
indexes = ((points - minp) / d).astype('int32')
# add point indices in points array
indexes = np.append(indexes, np.arange(points.shape[0], dtype='int32').reshape(points.shape[0], 1), axis=1)
print("--- indexing {} seconds ---".format((time.time() - start_time1)))

# create grid selecting points in grid cells
# create ESRI ASCII grid output
start_time2 = time.time()
oname = os.path.splitext(fname)[0] + ".asc"
f = open(oname, "w")
f.write("ncols {}\n".format(n[0]))
f.write("nrows {}\n".format(n[1]))
f.write("xllcorner {:.3f}\n".format(minp[0]))
f.write("yllcorner {:.3f}\n".format(minp[1]))
f.write("cellsize {:.3f}\n".format(d[0]))
f.write("nodata_value {:.3f}\n".format(no_data))

for i in reversed(range(n[1])):
    ii = indexes[indexes[:, 1] == i]     # points in the ith row of buckets
    for j in range(n[0]):
        jj = ii[ii[:, 0] == j]           # points in the single bucket
        pp = points[jj[:, 3]]
        if pp.size:
            gr = fu(pp[:, 2])     # apply min/max/mean/median
            f.write("{:.3f} ".format(gr))
        else:
            f.write("{:.3f} ".format(no_data))
    f.write("\n")
f.close()
print("--- griding1 {} seconds ---".format((time.time() - start_time2)))
# scanning sorted points
start_time3 = time.time()
# sorting indices array by bucket indices, decreasing rows and increasing cols
sorted_indexes = indexes[np.lexsort((indexes[:, 3], indexes[:, 2],
                                     indexes[:, 0], -indexes[:, 1]))]
oname = os.path.splitext(fname)[0] + "_1.asc"
f = open(oname, "w")
f.write("ncols {}\n".format(n[0]))
f.write("nrows {}\n".format(n[1]))
f.write("xllcorner {:.3f}\n".format(minp[0]))
f.write("yllcorner {:.3f}\n".format(minp[1]))
f.write("cellsize {:.3f}\n".format(d[0]))
f.write("nodata_value {:.3f}\n".format(no_data))
# buffer for a row of grid
grid = np.empty((n[0]))
grid.fill(no_data)
i = sorted_indexes[0, 1]
j = sorted_indexes[0, 0]
start = 0
m = sorted_indexes.shape[0]        # number of points
for k in range(m):
    # grid distance in row order of cells
    gd = -sorted_indexes[k, 1] * n[0] + sorted_indexes[k, 0] + i * n[0] - j
    if gd:
        # new bucket reached
        try:                    # TODO index out of range error
            grid[j] = fu(points[sorted_indexes[start:k, 3], 2])
        except IndexError:
            pass
        for ii in range(sorted_indexes[k, 1], i):
            for jj in range(n[0]):
                f.write("{:.3f} ".format(grid[jj]))
            f.write("\n")
            grid.fill(no_data)      # initialize row buffer
        j = sorted_indexes[k, 0]
        i = sorted_indexes[k, 1]
        start = k
# set last bucket
try:
    grid[j] = fu(points[sorted_indexes[start:m, 3], 2])
except IndexError:
    pass
for jj in range(n[0]):              # output a row to grid
    f.write("{:.3f} ".format(grid[jj]))
f.write("\n")
f.close()

print("--- griding2 {} seconds ---".format((time.time() - start_time3)))
start_time4 = time.time()
# scanning unsorted points
grid = {}
for i in range(n[1]):
    for j in range(n[0]):
        grid[(i, j)] = []    # initialize dict with empty lists
m = indexes.shape[0]        # number of points
for k in range(m):
    try:                     # TODO index out of range error
        grid[(indexes[k, 1], indexes[k, 0])].append(points[k, 2])
    except KeyError:
        pass

oname = os.path.splitext(fname)[0] + "_2.asc"
# output
f = open(oname, "w")
f.write("ncols {}\n".format(n[0]))
f.write("nrows {}\n".format(n[1]))
f.write("xllcorner {:.3f}\n".format(minp[0]))
f.write("yllcorner {:.3f}\n".format(minp[1]))
f.write("cellsize {:.3f}\n".format(d[0]))
f.write("nodata_value {:.3f}\n".format(no_data))
for i in reversed(range(n[1])):
    for j in range(n[0]):
        if len(grid[i, j]) > 0:
            f.write("{:.3f} ".format(fu(np.array(grid[(i, j)]))))
        else:
            f.write("{:.3f} ".format(no_data))
    f.write("\n")
f.close()
print("--- griding3 {} seconds ---".format((time.time() - start_time4)))
print("--- total {} seconds ---".format((time.time() - start_time)))
