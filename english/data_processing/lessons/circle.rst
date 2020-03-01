Regression circle
=================

*Keywords*: regression

*Data files*: circletest.txt, circletest1.txt

*Program files*: circle.m, circle1.m circle.py

A set of observed points are in a section of a circular object. Let's find
the best fitting circle (center point and radius) to these points.

.. code::

    (x - x0)^2 + (y - y0)^2 = r^2
    x^2 - 2x x0 + x0^2 + y^2 - 2y y0 + y0^2 = r^2
    y^2 + x^2 - 2x0 x - 2y0 y + x0^2 + y0^2 - r^2 = 0
    a1 = -2x0
    a2 = -2y0
    a3 = x0^2 + y0^2 - r^2
    y^2 + x^2 + a1 x + a2 y + a3 = 0

Let's solve the last equation for the a1, a2, a3 unknowns.
Original code can be found at http://www.mathworks.com/matlabcentral/fileexchange/5557-circle-fit/content/circfit.m

Octave solution (circle.m)
--------------------------

.. code:: octave

    % circle fit
    % x^2+y^2+a(1)*x+a(2)*y+a(3)=0
    x = [ 11.88; 10.34; 2.58; -0.29 ];
    y = [  0.08;  8.59; 9.54;  1.95 ];
    a = [x y ones(size(x))]\[-(x.^2+y.^2)];
    xc = -0.5*a(1)
    yc = -0.5*a(2)
    r  =  sqrt((a(1)^2+a(2)^2)/4-a(3))

Let's modify the code to read data from an input file, x and y coordinates in 
a row. The file name can be given in the command line or use default 
circletest.txt. (circle1.m)

.. code:: octave

    % circle fit coordinate file
    % read data from ascii file
    args = argv();
    if rows(args) == 0
        fname = 'circletest.txt';
    else
        fname = args{1};
    end
    points = dlmread(fname);
    a=[points(:,1) points(:,2) ones(rows(points),1)]\[-(points(:,1).^2+points(:,2).^2)];
    xc = -.5*a(1)
    yc = -.5*a(2)
    R  =  sqrt((a(1)^2+a(2)^2)/4-a(3))

Python solution (circle.py)
---------------------------

In the Python solution numpy is used.

.. code:: python

	import sys
	import math
	import numpy as np

	if len(sys.argv) > 1:
		fn = sys.argv[1]
	else:
		fn = 'circletest.txt'
	x1 = []
	y1 = []
	# load x,y data from file into lists
	with open(fn, 'r') as fp:
		for line in fp:
			l = line.strip().split()
			x1.append(float(l[0]))
			y1.append(float(l[1]))
	x = np.array(x1)        # create numpy array from x coords
	y = np.array(y1)        # create numpy array from y coords
	b = -(x * x + y * y)    # create pure terms
	ones = np.array([1.0] * np.size(x)) # build coefficient matrix
	a = np.append(x, y)
	a = np.append(a, ones)
	# solve least squares
	par = np.linalg.lstsq(a.reshape(3, np.size(x)).T, b)
	# get original variables
	xc = -0.5 * par[0][0]
	yc = -0.5 * par[0][1]
	R = math.sqrt((par[0][0] ** 2 + par[0][1] ** 2) / 4.0 - par[0][2])
	print('{:.3f} {:.3f} {:.3f}'.format(xc, yc, R))
