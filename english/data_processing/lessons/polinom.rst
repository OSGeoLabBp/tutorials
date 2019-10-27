Polynom interpolation
=====================

*Keywords*: interpolation, polynom

*Data file*: parabola.csv

*Program files*: parabola.m, parabola1.m, parabola_lsm.m

Let's fit a parabola through three points. First we create a program using the
traditional c/Java logic, in a second solution the more effective vetorization
method is used.

*Traditional solution* (parabola.m):

.. code:: octave

    % coordinates of points
    xp = [0; 21; 30];
    yp = [0; 55; 75];
    % set up equations
    A = zeros(3, 3);
    l = zeros(3, 1);
    for i=1:3
        A(i,1) = 1;
        A(i,2) = xp(i);
        A(i,3) = xp(i)^2;
        l(i) = yp(i);
    end
    x = inv(A) * l
    printf('Check\n')
    for i=1:3    % substitute original coordinates
      A(i,:) * x - yp(i)
    end

*Results*:

.. code:: text

    x =
       0.00000
       2.89683
      -0.01323

    Check
    ans = 0
    ans =  1.4211e-14
    ans =  1.4211e-14


*Vectorized solution* (parabola1.m):

.. code:: octave

    % coordinates of points
    xp = [0; 21; 30];
    yp = [0; 55; 75];
    % set up equations
    A = [ones(3,1), xp, xp .^ 2];    
    l = yp;
    x = A \ l
    printf('Check\n')
    polyval(flipud(x), xp)

Vectorization means that matrix operations are used instead of loop. This way
we get more compact, faster and more readble program.

*Result*:

.. code:: text

    x =
       0.00000
       2.89683
      -0.01323

    Check
    ans =
       0
       0
       0

Let's extend our solution to read points from data file and use a least squares
estimation for the parameters of the parabola. (parabola_lsm.m)

.. code:: octave

    % command line arguments
    args = argv();
    % open input file
    if (length(args))
        fp = fopen(args{1}, 'r');
    else
        fp = fopen('parabola.csv', 'r');
    end
    % load all coordinates
    points = sortrows(fscanf(fp, '%f;%f', [2, Inf])');
    n = rows(points);
    if (n < 4 )
        printf('Few points in input file\n');
    else
        A = [ones(n,1), xp, xp .^ 2];
        l = points(:, 2);
        x = A \ l
        rms = sqrt(sum((polyval(flipud(x), points(:, 1)) - points(:, 2)) .^ 2) / n);
        printf('RMS = %.3f\n', rms);
        plot(points(:, 1), points(:, 2), 'o');
        hold all;
        plot(points(1, 1):1:points(n, 1), polyval(flipud(x), points(1, 1):1:points(n, 1)), '-');
        legend('base points', 'approx. poly', 'location', 'southeast');
        hold off;
    end

|parabola_png|

.. |parabola_png| image:: images/parabola.png

Octave has a built-in function to fit a polynom called polyfit. Let's rewrite 
our code using built-in function (parabola_builtin.m).

.. code:: octave

    % command line arguments
    args = argv();
    % open input file
    if (length(args))
        fp = fopen(args{1}, 'r');
    else
        fp = fopen('parabola.csv', 'r');
    end
    % load all coordinates
    points = sortrows(fscanf(fp, '%f;%f', [2, Inf])');
    n = rows(points);
    if (n < 4 )
        printf('Few points in input file\n');
    else
      p = polyfit(points(:, 1), points(:, 2), 2)
        rms = sqrt(sum((polyval(p, points(:, 1)) - points(:, 2)) .^ 2) / n);
        printf('RMS = %.3f\n', rms);
        plot(points(:, 1), points(:, 2), 'o');
        hold all;
        plot(points(1, 1):1:points(n, 1), polyval(p, points(1, 1):1:points(n, 1)), '-');
        legend('base points', 'approx. poly', 'location', 'southeast');
        hold off;
    end

*Python/numpy solution (parabola.py)*

.. code:: python

	import sys
	import numpy as np
	import numpy.polynomial.polynomial as poly
	import matplotlib.pyplot as plt

	# read input data
	fn = 'parabola.csv'
	if len(sys.argv) > 1:
		fn = sys.argv[1]
	f = open(fn, 'r')
	x = []
	y = []
	for line in f:
		l = line.strip().split(';')
		x.append(float(l[0]))
		y.append(float(l[1]))
	coefs = poly.polyfit(x, y, 2)
	x_new = np.linspace(x[0], x[-1], num=len(x)*10)
	ffit = poly.polyval(x_new, coefs)
	plt.plot(x, y, 'ro')
	plt.plot(x_new, ffit)
	plt.show()

.. note:: *Development tipps*:

    Use higher order polynom, the order be an input
    Beautify plot, title, grid, etc.
    Try splinefit built-in function
