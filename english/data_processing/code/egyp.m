% process observation data for a point
% input file format: yyyy-mm-dd hh:mm:ss.sss WCB VA SD
f = fopen('egyp.txt', 'r');
% read data into a matrix
[data, n] = fscanf(f, '%d-%d-%d %d:%d:%f %f %f %f', [9, Inf]);
fclose(f);
data = data';   % transpose input matrix
[rows, cols] = size(data);
% convert date-time to days
data(:,1) = datenum(data(:,1), data(:,2), data(:,3), data(:,4), data(:,5), data(:,6));
% calculate offset from start time
data(:,1) = data(:,1) .- data(1,1);
% calculate coordinates
data(:, 2) = data(:, 9) .* sin(data(:, 8)) .* sin(data(:, 7));  % Easting
data(:, 3) = data(:, 9) .* sin(data(:, 8)) .* cos(data(:, 7));  % Northing
data(:, 4) = data(:, 9) .* cos(data(:, 8));                     % Elevation
% basic statistics
y = mean(data(:, 2));   % average
x = mean(data(:, 3));
z = mean(data(:, 4));
my = std(data(:, 2));   % standard deviation
mx = std(data(:, 3));
mz = std(data(:, 4));
printf('  Y[m]     X[m]     Z[m]     my[mm] mx[mm] mz[mm] skew\n');
printf('%8.4f %8.4f %8.4f %6.2f %6.2f %6.2f %6.2f %6.2f %6.2f\n', \
y, x, z, my * 1000, mx * 1000, mz * 1000, skewness(data(:,2)), \
skewness(data(:,3)), skewness(data(:,4)));
% normality
figure();
hist(data(:,2),500,1);
title('Y histogram');
xlabel('Y[m]');
ylabel('P');
figure();
hist(data(:,3),500,1);
title('X histogram');
xlabel('X[m]');
ylabel('P');
figure();
hist(data(:,4),500,1);
title('Z histogram');
xlabel('Z[m]');
ylabel('P');
% correlations
cy = cov(data(:,1), data(:,2)) / std(data(:,1)) / std(data(:,2));
cx = cov(data(:,1), data(:,3)) / std(data(:,1)) / std(data(:,3));
cz = cov(data(:,1), data(:,4)) / std(data(:,1)) / std(data(:,4));
cyx = cov(data(:,2), data(:,3)) / std(data(:,2)) / std(data(:,3));
cyz = cov(data(:,2), data(:,4)) / std(data(:,2)) / std(data(:,4));
cxz = cov(data(:,3), data(:,4)) / std(data(:,3)) / std(data(:,4));
printf('\n     Correlations\n');
printf('      Y     X     Z\n');
printf('time %5.3f %5.3f %5.3f\n', cy, cx, cz);
printf('   Y  -    %5.3f %5.3f\n', cyx, cyz);
printf('   X  -     -    %5.3f\n', cxz);
% looking for linear trend
py = polyfit(data(:,1), data(:,2), 1);
px = polyfit(data(:,1), data(:,3), 1);
pz = polyfit(data(:,1), data(:,4), 1);
ty = py(1) * data(:,1) + py(2);
tx = px(1) * data(:,1) + px(2);
tz = pz(1) * data(:,1) + pz(2);
figure();
plot(data(:,1), ty);
hold all;
plot(data(:,1), data(:,2));
title ('time - Y');
figure();
plot(data(:,1), tx);
hold all;
plot(data(:,1), data(:,3));
title ('time - X');
figure();
plot(data(:,1), tz);
hold all;
plot(data(:,1), data(:,4));
title ('time - Z');
