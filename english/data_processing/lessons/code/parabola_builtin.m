% command line arguments
args = argv();
% load all coordinates
fname = 'parabola.csv';
for i = 1:length(args)
  if args{i}(1) != '-'
	  fname = args{1};
    break;
  end
end
points = dlmread(fname);
n = rows(points);
p = polyfit(points(:, 1), points(:, 2), 2)
rms = sqrt(sum((polyval(p, points(:, 1)) - points(:, 2)) .^ 2) / n);
printf('RMS = %.3f\n', rms);
plot(points(:, 1), points(:, 2), 'o');
hold all;
plot(points(1, 1):1:points(n, 1), polyval(p, points(1, 1):1:points(n, 1)), '-');
legend('base points', 'approx. poly', 'location', 'southeast');
hold off;
