% fit sphere through 4 non coplanar points
points = dlmread('sphere4p.txt',',');   % separator is comma
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
r = sqrt(x0^2 + y0^2 + z0^2 - dM15/dM11);
printf('x0=%.3f y0=%.3f z0=%.3f r=%.3f\n', x0, y0, z0, r);

