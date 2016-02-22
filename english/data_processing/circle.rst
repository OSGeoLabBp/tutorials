Regression circle
=================

A set of observed points are in a section of a circular object. Let's find
the best fitting circle (center point and radius) to these points.

.. code::

    (y - y0)^2 + (x - x0)^2 = r^2
    y^2 - 2y y0 + y0^2 + x^2 - 2x x0 + x0^2 = r^2
    y^2 + x^2 -2y0 y - 2x0 x + y0^2 + x0^2 - r^2 = 0
    a1 = -2y0
    a2 = -2x0
    a3 = y0^2 + x0^2 - r^2
    y^2 + x^2 + a1 y + a2 x + a3 = 0

Let's solve the last equation for the a1, a2, a3 unknowns in Octave.

.. code::

    % circle fit
    % x^2+y^2+a(1)*x+a(2)*y+a(3)=0
    x = [ 11.88; 10.34; 2.58; -0.29 ];
    y = [  0.08;  8.59; 9.54;  1.95 ];
    a = [x y ones(size(x))]\[-(x.^2+y.^2)];
    xc = -0.5*a(1)
    yc = -0.5*a(2)
    r  =  sqrt((a(1)^2+a(2)^2)/4-a(3))

