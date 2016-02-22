% command line arguments
args = argv();
% open input file
if (length(args))
	fp = fopen(args{1}, 'r');
else
	fp = fopen('parabola.csv', 'r');
end
% load all coordinates
points = sortrows(fscanf(fp, '%f;%f', [2, Inf])');
n = rows(points);
if (n < 4 )
	printf("Few points in input file\n");
else
	A = [ones(n, 1), points(:, 1), points(:, 1) .^ 2];
	l = points(:, 2);
	x = A \ l
	rms = sqrt(sum((polyval(flipud(x), points(:, 1)) - points(:, 2)) .^ 2) / n);
	printf('RMS = %.3f\n', rms);
	plot(points(:, 1), points(:, 2), 'o');
	hold all;
	plot(points(1, 1):1:points(n, 1), polyval(flipud(x), points(1, 1):1:points(n, 1)), '-');
	legend('base points', 'approx. poly', 'location', 'southeast');
	hold off;
end
