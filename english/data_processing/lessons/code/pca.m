% rotated ellipse
pkg load statistics
points = dlmread('ellipse.txt');
% eigen vectors & rotated, shifted points
[a, b] = princomp(points);
% shift of points
x0 = mean(points(:, 1)) - mean(b(:, 1));
y0 = mean(points(:, 2)) - mean(b(:, 2));
% rotational angle
alpha = atan2(a(2, 1), a(1, 1));
% run ellipse for b
%[d, e] = eig(c)
plot(points(:,1), points(:, 2));
hold on
plot([0, a(1, 1)], [0, a(2, 1)]);
plot([0, a(1, 2)], [0, a(2, 2)]);
plot(b(:,1), b(:, 2));
