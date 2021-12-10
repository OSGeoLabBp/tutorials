% horizontal free network adjustment
% point numbers should be 1, 2, 3, etc.

format long
std_dist = 0.001; % mean error of distances im meters
std_dir = 0.0006 / 200 * pi;  % mean error of directions in radians
p_dist = 1.0 / std_dist**2;
p_dir = 1.0/ std_dir**2;
% load preliminary coordinates: Y, X or ID, Y, X 
coords = dlmread('coords.txt', ',');
if (columns(coords) > 2)
  coords = coords(:, 2:3);
end
% load distances: from , to, horizontal distance
dists = dlmread('dists.txt', ',');
% load directions: from, to, mean direction in GONs
dirs = dlmread('dirs.txt', ',');
% load preliminary orientations: point, orientation angle or orientation angle
oris = dlmread('oris.txt', ',');
if (columns(oris) > 1)
  oris = oris(:, 2);
end
% set up A matrix and pure term (l)
m = rows(dists) + rows(dirs);
n = rows(coords) * 3;  % free network, all points were station
stn = rows(oris);
A = zeros(m, n);
l = zeros(m,1);
P = zeros(m, m);
% process distances
for i = 1:rows(dists)
  p1 = dists(i, 1);
  p2 = dists(i, 2);
  dist = sqrt((coords(p2, 1) - coords(p1, 1)) ** 2 + (coords(p2, 2) - coords(p1, 2)) ** 2);
  c = (coords(p2, 1) - coords(p1, 1)) / dist;
  d = (coords(p2, 2) - coords(p1, 2)) / dist;
  j1 = stn + dists(i, 1) * 2 - 1;
  j2 = stn + dists(i, 2) * 2 - 1;
  A(i, j1) = -c;
  A(i, j2) = c;
  A(i, j1+1) = -d;
  A(i, j2+1) = d;
  l(i) = dist - dists(i, 3);
  P(i, i) = p_dist;
end
% process mean directions
for i = 1: rows(dirs)
  p1 = dists(i, 1);
  p2 = dists(i, 2);
  wcb = atan2(coords(p2, 1) - coords(p1, 1), coords(p2, 2) - coords(p1, 2));
  if (wcb < 0)
    wcb += 2 * pi;
  end
  dist = sqrt((coords(p2, 1) - coords(p1, 1)) ** 2 + (coords(p2, 2) - coords(p1, 2)) ** 2);
  a = (coords(p2, 2) - coords(p1, 2)) / dist**2;
  b = (coords(p2, 1) - coords(p1, 1)) / dist**2;
  j1 = stn + dists(i, 1) * 2 - 1;
  j2 = stn + dists(i, 2) * 2 - 1;
  ii = rows(dists) + i;
  A(ii, p1) = -1.0;  % orientations
  A(ii, j1) = -a;
  A(ii, j2) = a;
  A(ii, j1+1) = -b;
  A(ii, j2+1) = b;
  l(ii) = (dirs(i, 3) + oris(p1)) / 200.0 * pi - wcb;
  P(ii, ii) = p_dir;
end
% LSM
N = A' * P * A;
Ninv = pinv(N);
f = m - rank(N);        % number of redundant observations
x = Ninv * A' * P * l;  % change of preliminary values
v = A * x - l;          % corrections
m0 = sqrt((v' * P * v) / f);
w1 = v' * P * v;
w2 = -l' * P * v;
% output
printf('Check of calculation: %.5f = %.5f?\n', w1, w2);
printf('m0 = %5.2f\n', m0);
printf('\nOrientation unknowns [GON]\n');
printf('Station  Prelim  Change Adjusted\n');
for i = 1:rows(oris)
  printf('%6d %8.4f %6.4f %8.4f\n', i, oris(i), x(i) * 200.0 / pi, oris(i) + x(i) * 200.0 / pi);
end
printf('\nAdjusted coordinates [m]\n');
printf('Point            Prelim             Change              Adjusted\n')
for i = 1:rows(coords)
  j = stn + i * 2 - 1;
  printf('%5d %12.3f,%12.3f %6.3f,%6.3f %12.3f,%12.3f\n', i, coords(i, 1), coords(i, 2), x(j), x(j+1), coords(i, 1)+x(j), coords(i, 2)+x(j+1));
end
printf('\nCorrections and observations\n');
printf('Distances [m]\n');
printf('From   To Measured    Corr    Adjusted\n');
for i = 1:rows(dists)
  p1 = dists(i, 1);
  p2 = dists(i, 2);
  printf('%4d %4d %8.3f  %7.3f  %8.3f\n', p1, p2, dists(i, 3), v(i), dists(i, 3)+v(i));
end
printf('\nDirections [GON]\n');
printf('From   To  Measured   Corr    Adjusted\n');
for i = 1:rows(dirs)
  p1 = dists(i, 1);
  p2 = dists(i, 2);
  v_gon = v(rows(dists) + i) * 200.0 / pi;
  printf('%4d %4d %9.4f  %7.4f %9.4f\n', p1, p2, dirs(i, 3), v_gon, dirs(i, 3)+v_gon);
end
