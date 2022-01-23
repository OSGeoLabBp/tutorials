Regression sphere
=================

*Data files*: sphere1.txt
*Program files*: sphere.m, sphere.py

A set of observed points are on a sphere. Let's find
the best fitting sphere (center point and radius) to these points.

.. code::

    (x - x0)^2 + (y - y0)^2 + (z - z0)^2 = r^2
    x^2 - 2x x0 + x0^2 + y^2 - 2y y0 + y0^2 + z^2 -2z z0 + z0^2 = r^2
    y^2 + x^2 + z^2 - 2x0 x - 2y0 y -2z0 z + x0^2 + y0^2 + z0^2 - r^2 = 0
    a1 = -2x0
    a2 = -2y0
    a3 = -2z0
    a4 = x0^2 + y0^2 + z0^2 - r^2
    y^2 + x^2 + z^2 + a1 x + a2 y + a3 z + a4 = 0

This solution is similar to the method used for circle fitting. Substitutions
were used to have linear equation system for a1, a2, a3, a4, from these the
center point coordinates (x0, y0, z0) can be calculated and then the radius.

Octave solution
---------------

The above formulas are used for points read from text file.

.. code::

	% sphere fit
	% x^2 + y^2 + z^2 + a(1) * x + a(2) * y + a(3) * z + a(4)
	points = dlmread('sphere1.txt');
	x = points(:,2);
	y = points(:,3);
	z = points(:,4);
	a = [x y z ones(rows(x), 1)] \ [-(x.^2 + y.^2 + z.^2)];
	x0 = -0.5 * a(1);
	y0 = -0.5 * a(2);
	z0 = -0.5 * a(3);
	R = sqrt((a(1)^2 + a(2)^2 + a(3)^2) / 4.0 - a(4));
	printf('%.2f %.2f %.2f %.2f\n', x0, y0, z0, R);
	d = sqrt((x .- x0).^2 + (y .- y0).^2 + (z .- z0).^2) .-R;
	rms = sqrt(sum(d.^2) / rows(x))

A vectorized solution is given above and the RMS value is calculated too.
The RMS value reflects the goodness of the sphere fitting.

Results of the program:

.. code::

    101.98 99.72 58.19 0.28
    rms =    5.5532e-12

Python/numpy solution
---------------------

In this Python code more input files are handled from the command line.
The code for a sphere fitting is put into a function (*sphere*).

.. code:: python

    import numpy as np
    from math import sqrt
    from sys import argv

    def sphere(x_, y_, z_):
        """
            calculate best fitting sphere (LSM) on points
            :param returns: x0, y0, z0, R
        """
        n_ = x_.shape[0]
        a = np.c_[x_, y_, z_, np.full(n_, 1, 'float64')]
        b = -np.square(x_) - np.square(y_) - np.square(z_)
        res = np.linalg.lstsq(a, b, rcond=None)[0]
        return -0.5 * res[0], -0.5 * res[1], -0.5 * res[2], \
              sqrt((res[0]**2 + res[1]**2 + res[2]**2) / 4 - res[3])

    if __name__ == "__main__":
        if len(argv) > 1:
            file_names = argv[1:]
        else:
            file_names = ['sphere1.txt']
        for file_name in file_names:
            pnts = np.genfromtxt(file_name, 'float64', delimiter=',')
            if pnts.shape[1] > 3:
                pnts = pnts[:,1:4]  # skip first column (point id)
            sph = sphere(pnts[:,0], pnts[:,1], pnts[:,2])
            print("x0: {:.3f} y0: {:.3f} z0: {:.3f} R: {:.3f}".format(sph[0], sph[1], sph[2], sph[3]))
            dr = np.sqrt(np.sum(np.square(pnts - sph[:3]), 1)) - sph[3] # difference in radius direction
            RMS = sqrt(np.sum(np.square(dr)) / pnts.shape[0])
            print("RMS: {:.3f}".format(RMS))

Results of the program using sphere1.txt:

.. code:: 

    x0: 101.985 y0: 99.725 z0: 58.187 R: 0.277
    RMS: 0.000

