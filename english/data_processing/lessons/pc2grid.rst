Converting point cloud to ASCII grid
====================================

*Keywords*: point cloud, effective algorithm, spatial indexing
*Data files*: pc_sample.txt
*Program files*: pc2grid.py

In this tutorial we shell demostrate three different approache to
generate ASCII grid from an ASCII point cloud file.
Depending on the number of points and the GRID resolution different
algorithms are the most effective.

After loading the points an index list is generated, the zero based grid row and
column number is calculated for each point.

Data structures used:

- points: 2D numpy array [[x1, y1, z1] [x2, y2, z2] ...]
- indexes: 2D numpy array [[grid_col, grid_row, grid_z, pointd_index], ...]

The input is a whitespace separated ASCII point cloud file. The X, Y, Z 
coordinates have to be in the first three columns, what extra columns can follow
(e.g. colour, normat etc.).

The output is an ESRI ASCII grid file what several GIS programs can load, among
others QGIS, GRASS GIS, SAGA GIS.

The solutions are heavely based on numpy functionality.
Now we disscuss some interesting parts of the code.

At the beginning some command line parameters are processed. The third
parameter is a name for the function to calculate the grid cell value from
the points inside it. Here we assign the address of the function to variable
*fu* and later this is used to call the necessary function. We suppose the
parameter of these functions is a numpy vector (vector of Z coordinates).

After loading the coordinates and deleting extra columns, an index is build 
using numpy operation on array.

.. code:: python

        # get extent
        minp = np.amin(points, axis=0)
        maxp = np.amax(points, axis=0)
        # round to grid values
        minp = np.floor(minp / d) * d
        maxp = np.ceil(maxp / d) * d
        # number of buckets along the axicis
        n = ((maxp - minp) / d).astype('int32')
        # creating index bucket rows and columns
        indexes = ((points - minp) / d).astype('int32')
        # add point indices in points array
        indexes = np.append(indexes, np.arange(points.shape[0],
                  dtype='int32').reshape(points.shape[0], 1), axis=1)

All the operations are vectorized in the code above (instead of loops array
operartions are used). First we get the extent of the point cloud along the
three axes, minp and maxp are vectors of three values. Than the extent is 
enlarged to be on grid border (grid step is *d*).
In the next row the sizes of the grid is calculated (in Z direction also,
which will not be used later). We create an extra array with the 
grid indices for each points. The indexec are integer values that is the
reason to have a new array with integer elements beside the points array of
float elements. Finally the the point indexes are added to this array, which is
used in the 1st and 2nd algorithm to refer back o the correcponding points.

1st variant
-----------

For each cell in the GRID we select the elevations of internal points.
The GRID output is built cell by cell and written direcly to the
output file.

.. code:: python

        for i in reversed(range(n[1])):
            ii = indexes[indexes[:,1] == i]     # points in the ith row of buckets
            for j in range(n[0]):
                jj = ii[ii[:,0] == j]           # points in the single bucket
                pp = points[jj[:,3]]
                if pp.size:
                    gr = fu(pp[:,2])            # apply min/max/mean/median
                    f.write("{:.3f} ".format(gr))
                else:
                    f.write("{:.3f} ".format(no_data))
            f.write("\n")

The external loop goes through the rows in reverse order because in the ASCII 
grid file the first row is the top most row of the grid (in our grid indexing
schema the first row is the bottom most). Then we select from the index array
the points in the *ith* row (*ii* array). In the internal loop we go through 
columns and select the points in *jth* column from the points in the row.
We get the point indices using the 3rd column of index, which his the 
point index in the *points* array. So *pp* is the array of points inside the
*ith* row and *jth* column cell of grid. Finally the selected function (min,
max, mean, etc.) is used for Z coordinates to get the cell value (*gr*) if
there are points in the cell otherwise *NO DATA* value is written to the
output.

2nd variant
-----------

We sort the index array by cell rows and columns, so one sequential scan of
points enough to calculate cell values. The sorting is made by the lexsort 
function, where the last parameter is the primary sorting key. We used negative
sign to sort rows in decreasing order because in the ASCII
grid file the first row is the top most row of the grid (in our grid indexing
schema the first row is the bottom most).

The GRID output is generated row by row, one row is buffered before write, to
handle empty cells.

.. code:: python

        grid = np.empty((n[0]))
        grid.fill(no_data)
        i = sorted_indexes[0,1]
        j = sorted_indexes[0,0]
        start = 0
        m = sorted_indexes.shape[0]        # number of points
        for k in range(m):
            # grid distance in row order of cells
            gd = -sorted_indexes[k,1] * n[0] + sorted_indexes[k,0] + i * n[0] - j
            if gd:
                # new bucket reached
                try:                    # TODO index out of range error
                    grid[j] = fu(points[sorted_indexes[start:k,3],2])
                except:
                    pass
                for ii in range(sorted_indexes[k,1], i):
                    for jj in range(n[0]):
                        f.write("{:.3f} ".format(grid[jj]))
                    f.write("\n")
                    grid.fill(no_data)
                j = sorted_indexes[k,0]
                i = sorted_indexes[k,1]
                start = k
        # set last bucket
        try:
            grid[j] = fu(points[sorted_indexes[start:m,3],2])
        except:
            pass
        for jj in range(n[0]):
            f.write("{:.3f} ".format(grid[jj]))
        f.write("\n")

First we initialize the grid row buffer with *NO DATA* values and take the
grid indices of the left most point in the upper left cell (*i* and *j*).
The *start* variable stores the beginning of the actual grid cell in the
indices. We have a single loop on the sorted indices. In the *gd* variable the
grid distance is calculated between the actual cell (*i*, *j*) and the *kth* 
point in the index. If the grid distance is zero (point is in the actual cell)
nothing is done. Otherwise the cell value is calcuted from the range of points
from start to actual index (*k*) but one. The loop for *ii* is necessary if 
there are empty grid rows to write more rows into the output. 
At the and of this part the actual cell indices and *start* index is updated.
After this loop the last row is in the buffer, so we write that out, too.

3rd variant
-----------

In this variant the points are scanned only once.
The whole GRID output is generated in memory using unsorted index. 
As the append values to a numpy array is not effective enough a dictionary is
created where the indices are tuples of row and column indises the grid and
the stored value in the dictionary members is the list of Z values in that cell.

.. code:: python

        grid = {}
        for i in range(n[1]):
            for j in range(n[0]):
                grid[(i,j)] = []    # initialize dict with empty lists
        m = indexes.shape[0]        # number of points
        for k in range(m):
            try:                     # TODO index out of range error
                grid[(indexes[k,1],indexes[k,0])].append(points[k,2])
            except:
                pass

At the beginning we initialize the dictionary with emply list, so we can
append values later. Then in the loop for *k* we simply append Z coordinate
of the actual point to the corresponding grid cell. While the points are 
unsorted we can output the grid after processing all points in an extra 
double loop.

Performance
-----------

The performance of the algorithms were tested on two moderate size point cloud.

First test with a point cloud of 1.1 M points created from drone images.
Average distance among points is 2 cm. The test war run with five different
resolutions.

+------------+------+------+-------+-------+--------+
| resolution | 10 m |  5 m |   1 m | 0.1 m | 0.05 m |
+------------+------+------+-------+-------+--------+
| 1st        | 0.08 | 0.10 |  0.29 | 3.50  | 9.24   |
+------------+------+------+-------+-------+--------+
| 2nd        | 1.16 | 1.18 |  1.23 | 2.04  | 5.05   |
+------------+------+------+-------+-------+--------+
| 3rd        | 2.95 | 2.97 |  2.96 | 3.84  | 7.70   |
+------------+------+------+-------+-------+--------+

Second test with a 4 M pointi cloudr, 1 point / sq m.

+------------+-------+-------+-------+-------+
| resolution |  20 m |  10 m |   5 m |   1 m |
+------------+-------+-------+-------+-------+
| 1st        |  2.11 |  4.60 | 10.81 | 96.55 |
+------------+-------+-------+-------+-------+
| 2nd        |  6.01 |  6.24 |  7.30 | 36.87 |
+------------+-------+-------+-------+-------+
| 3rd        | 14.77 | 14.98 | 16.70 | 38.15 |
+------------+-------+-------+-------+-------+

*Development tipp*

Try to speed up the algorithms demostrated or try to find faster algorithms.

Create Octave/Matlab script for the algorithms and compare the speed to 
Python.
