% sphere trough four points
r = 0.206;
points = dlmread('sphere1.txt');
x = points(:,2);
y = points(:,3);
z = points(:,4);
% plane through midpoint 1-2
p1 = [ (x(1) + x(2)) / 2, (y(1) + y(2)) / 2, (z(1) + z(2)) / 2];
pl1 = zeros(4,1);
pl1(1) = x(2) - x(1);
pl1(2) = y(2) - y(1);
pl1(3) = z(2) - z(1);
pl1(4) = -(p1 * pl1(1:3));
% plane through midpoint 3-4
p2 = [ (x(3) + x(4)) / 2, (y(3) + y(4)) / 2, (z(3) + z(4)) / 2];
pl2 = zeros(4,1);
pl2(1) = x(4) - x(3);
pl2(2) = y(4) - y(3);
pl2(3) = z(4) - z(3);
pl2(4) = -(p2 * pl2(1:3));
% intersection of two planes
