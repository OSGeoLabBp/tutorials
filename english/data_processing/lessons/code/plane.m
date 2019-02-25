% load points
points = dlmread('plane.txt');
n = rows(points);
wp = sum(points) / n;
y = points(:, 1) - wp(1);
x = points(:, 2) - wp(2);
z = points(:, 3) - wp(3);
a = zeros(3, 3);
a(1, 1) = sum(y .^2);
a(1, 2) = a(2, 1) = sum(y .* x);
a(1, 3) = a(3, 1) = sum(y .* z);
a(2, 2) = sum(x .^2);
a(2, 3) = a(3, 2) = sum(x .* z);
a(3, 3) = sum(z .^2);
[ev, l] = eig(a);
norm = ev(:, 1);
p = zeros(1,4);
p(4) = - wp * norm;
p(1) = norm(1);
p(2) = norm(2);
p(3) = norm(3);
% check
c = points * norm + p(4)