% sphere fit from file for four point
% x^2 + y^2 + z^2 + a(1) * x + a(2) * y + a(4) * z + a(4)
points = dlmread('gomb.csv');
for ind = 1:4:rows(points)
  i4 = ind + 3;
  x = points(ind:i4,2);
  y = points(ind:i4,3);
  z = points(ind:i4,4);
  a = [x y z ones(rows(x), 1)] \ [-(x.^2 + y.^2 + z.^2)];
  x0 = -0.5 * a(1);
  y0 = -0.5 * a(2);
  z0 = -0.5 * a(3);
  R = sqrt((a(1)^2 + a(2)^2 + a(3)^2) / 4.0 - a(4));
  d = sqrt((x .- x0).^2 + (y .- y0).^2 + (z .- z0).^2) .- R;
  rms = sqrt(sum(d.^2) / rows(x));
  printf('%d %.3f %.3f %.3f %.3f %.6f\n', points(ind,1), x0, y0, z0, R, rms);
end