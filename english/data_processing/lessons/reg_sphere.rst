Regression sphere
=================

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
