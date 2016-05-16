Regression circle
=================

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

Let's solve the last equation for the a1, a2, a3 unknowns in Octave.
Original code can be found at http://www.mathworks.com/matlabcentral/fileexchange/5557-circle-fit/content/circfit.m

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
circletest.txt.

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

