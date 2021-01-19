% find principal components
% sudo apt-get install octave-statistics
pkg load statistics
points = dlmread('pca.txt');
% step by step solution
means = mean(points);
Xd = points - means;
cov = Xd' * Xd;
[eig_vectors, eig_values] = eig(cov);
direction = atan2(eig_vectors[0][0], eig_vectors[1][0]) * 180 / pi;
printf("weight point: %.2f, %.2f\n", means(1), means(2))
printf("direction: %.1f\n", direction)
% eigen vectors & rotated, shifted points (b)
[eig_vectors, b, eig_values] = princomp(points);
% shift of points
x0 = mean(points(:, 1)) - mean(b(:, 1));
y0 = mean(points(:, 2)) - mean(b(:, 2));
% rotational angle
direction = atan2(eig_vectors(1, 1), eig_vectors(2, 1)) * 180. / pi();
printf("weight point: %.2f, %.2f\n", x0, y0)
printf("direction: %.1f\n", direction)
plot(points(:,1), points(:, 2), 'o');
hold on
plot(x0, y0, 'x')
plot([x0-eig_vectors(1,1)*10; x0; x0+eig_vectors(1,1)*10], ...
     [y0-eig_vectors(2,1)*10; y0; y0+eig_vectors(2,1)*10])
