% generate point on sphere with random noise
x0 = 1.5;
y0 = 2.5;
z0 = 3.5;
r = 6.2;
alfas = [0, pi/2., pi, 3 * pi / 2];
betas = [-pi/2.+0.1, -pi/4., 0, pi/4., pi/2.-0.1];
for i=1:columns(alfas)
	for j=1:columns(betas)
		x = x0 + r * cos(betas(j)) * sin(alfas(i)) + (2 * rand - 1) / 10;
		y = y0 + r * cos(betas(j)) * cos(alfas(i)) + (2 * rand - 1) / 10;
		z = z0 + r * sin(betas(j)) + (2 * rand - 1) / 10;
		printf("%d%d %.3f %.3f %.3f\n", i, j, x, y, z);
	end
end
