% fit sphere through 3 points with known radius
r = 6.840;    % fixed radius update as needed
points = dlmread('sphere4p.txt',',');   % separator is comma
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
printf('First solution: x0=%.3f y0=%.3f z0=%.3f\n', cs1);
printf('Second solution: x0=%.3f y0=%.3f z0=%.3f\n', cs2);
