Measure point with slope prism rod
==================================

To measure a point for example on a vertical plan with a total station can be done by
measuring three or four different points fixing the rod end at the point of 
interest. Three points are enough if the rod length is known.

*Keywords:* sphere fitting, determinant, submatrix

*Data file*: sphere4.txt

*Program files*: sphere4p.m, sphere3p.m

*Sample data (x, y, z), for sphere3p.m the first three points are used*

.. code:: text

    2,0,0
    0,2,0
    -2,0,0
    0,0,2

*matematical backgroud*

r^2 = (x - x0)^2 + (y - y0)^2 + (z - z0)^2

The solution details can be found at http://math.stackexchange.com/questions/894794/sphere-equation-given-4-points

*Octave solution* (sphere4.m)

.. code:: octave

    % fit sphere through 4 non coplanar points
    points = dlmread('sphere4p.txt',",");
    % first four points are used
    M=[points(1,1)^2+points(1,2)^2+points(1,3)^2,points(1,1),points(1,2),points(1,3),1;
       points(2,1)^2+points(2,2)^2+points(2,3)^2,points(2,1),points(2,2),points(2,3),1;
       points(3,1)^2+points(3,2)^2+points(3,3)^2,points(3,1),points(3,2),points(3,3),1;
       points(4,1)^2+points(4,2)^2+points(4,3)^2,points(4,1),points(4,2),points(4,3),1];
    dM11 = det(M(:,[2,3,4,5]));    % determinants of different submatrices
    dM12 = det(M(:,[1,3,4,5]));
    dM13 = det(M(:,[1,2,4,5]));
    dM14 = det(M(:,[1,2,3,5]));
    dM15 = det(M(:,[1,2,3,4]));
    x0 = 0.5 * dM12 / dM11;
    y0 =-0.5 * dM13 / dM11;
    z0 = 0.5 * dM14 / dM11;
    r = sqrt(x0^2 + y0^2 + z0^2 – dM15/dM11);
    printf("x0=%.3f y0=%.3f z0=%.3f r=%.3f\n", x0, y0, z0, r);

*Mathematical background*

The circuscribed circle through the three points is a section of the sphere. There are two possible solutions.

*Octave solution* (sphere3p.m)

.. code:: octave

    % fit sphere through 3 points with known radius
    r = 6.840;    % fixed radius update as needed
    points = dlmread("sphere4p.txt",',');   % separator is comma
    % first three points are used
    mp12 = (points(1,:) + points(2,:)) ./ 2;   % midpoint between point 1 and 2
    mp13 = (points(1,:) + points(3,:)) ./ 2;
    % plane perpendicular to 1-2 edge
    p12 = zeros(4,1);
    p12(1:3) = points(2,:) - points(1,:);   % normal vector of the plane
    p12(4) = -dot(p12(1:3), mp12);
    % plane perpendicular to 1-3 edge
    p13 = zeros(4,1);
    p13(1:3) = points(3,:) - points(1,:);   % normal vector of the plane
    p13(4) = -dot(p13(1:3), mp13);
    % plane through the three point
    p123 = zeros(4,1);
    p123(1:3) = cross(points(2,:) - points(1,:), points(3,:) - points(1,:));     % normal vector of the plane
    p123(1:3) = p123(1:3) ./ norm(p123(1:3),2);   % normalize normal vector
    p123(4) = -dot(p123(1:3), points(3,:));
    % center of circumscribed circle of the 3 points (intersection of three planes)
    cp1 = inv([p12, p13, p123, [0;0;0;1]])(4,:)'(1:3);
    cp = [0.7791; -0.9419;2.9884];
    dc1 = norm(cp - points(1,:)',2);   % distance from center to first point
    dcc = sqrt(r^2 - dc1^2);   % distance from cp to center of sphere
    % center of two spheres
    cs1 = cp + p123(1:3) .* dcc;
    cs2 = cp - p123(1:3) .* dcc;
    printf("First solution: x0=%.3f y0=%.3f z0=%.3f\n", cs1);
    printf("Second solution: x0=%.3f y0=%.3f z0=%.3f\n", cs2);

