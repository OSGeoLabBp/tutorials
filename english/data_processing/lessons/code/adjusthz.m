% horizontal free network adjustment
% point numbers should be ordinal numbers: 1, 2, 3, etc.
% coordinate list have to be sorted for point numbers
% all input angles are in GONs

format long
% **** UPDATE A PRIORI MEAN ERRORS ****
std_dist = 0.001; % mean error of distances im meters
std_dir = 0.0006; % mean error of directions in GON
% **** END UPDATEABLE PART ****
std_dir = std_dir / 200 * pi;  % mean error to radians
p_dist = 1.0 / std_dist**2;
p_dir = 1.0/ std_dir**2;
% load preliminary coordinates: Y, X or ID, Y, X 
coords = dlmread('coords.txt', ',');
if (columns(coords) > 2)
  coords = coords(:, 2:3);  % drop point ids as it is the index
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
m0 = sqrt((v' * P * v) / f);    % mean error of unit weight
quu = A * Ninv * A';
w1 = v' * P * v;
w2 = -l' * P * v;
% output
printf('Check of calculation: %.5f = %.5f?\n', w1, w2);
printf('m0 = %5.2f\n', m0);
printf('\nOrientation unknowns [GON]\n');
printf('Station  Prelim  Change Adjusted Mean error\n');
for i = 1:rows(oris)
  x_gon = x(i) * 200 / pi;
  oo = oris(i) + x_gon;
  if (oo < 0)
      oo += 400;
  end
  printf('%6d %8.4f %6.4f %8.4f %6.4f\n', i, oris(i), x_gon, oo, m0 * sqrt(Ninv(i, i)));
end
printf('\nAdjusted coordinates [m]\n');
printf('                Preliminary         Change\n')
printf('Point        East         North  East   North\n')
for i = 1:rows(coords)
  j = stn + i * 2 - 1;
  printf('%5d %12.3f,%12.3f %6.3f,%6.3f\n', i, coords(i, 1), coords(i, 2), x(j), x(j+1));
end
printf('\n                  Adjusted        Mean error\n')
printf('Point        East         North  East   North\n')
for i = 1:rows(coords)
  j = stn + i * 2 - 1;
  printf('%5d %12.3f,%12.3f %6.3f,%6.3f\n', i, coords(i, 1)+x(j), coords(i, 2)+x(j+1), m0 * sqrt(Ninv(j,j)), m0 * sqrt(Ninv(j+1,j+1)));
end
printf('\nCorrections and observations\n');
printf('Distances [m]\n');
printf('From   To Measured    Corr    Adjusted  Mean error\n');
for i = 1:rows(dists)
  p1 = dists(i, 1);
  p2 = dists(i, 2);
  printf('%4d %4d %8.3f  %7.3f  %8.3f  %7.3f\n', p1, p2, dists(i, 3), v(i), dists(i, 3)+v(i), m0 * sqrt(quu(i, i)));
end
printf('\nDirections [GON]\n');
printf('From   To  Measured   Corr    Adjusted  Mean error\n');
for i = 1:rows(dirs)
  p1 = dirs(i, 1);
  p2 = dirs(i, 2);
  j = rows(dists) + i;
  v_gon = v(j) * 200.0 * pi;
  dd = dirs(i, 3) + v_gon;
  if (dd < 0)
    dd += 400;
  end
  printf('%4d %4d %9.4f  %7.4f %9.4f  %7.4f\n', p1, p2, dirs(i, 3), v_gon, dd, m0 * sqrt(quu(j, j)));
end
