% get a slide from point cloud perpendicular to one of the axis
% of the co-ordinate system with a tolerance
% parameters:
%   fname - input coordinate file (default lidar.txt)
%   coo - coordinate of section (default 1000)
%   col - coordinate column (default 3)
%   tol - tolerance to co-ordinate (default 0.2)
%   sep - separator in input file (default ',')
args = argv();  % command line arguments in a cell array
n = nargin;
i = 1;
% skip switches
if n > 0
  while i <= nargin && args{i}(1) == '-'
    i += 1;
    n -= 1;
  end
end
 % check positional parameters
if n > 0
  fname = args{i};
else
  fname = 'lidar.txt';
end
if n > 1
  coo = str2num(args{i+1});
else
  coo = 1000;
end
if n > 2
  col = int32(str2num(args{i+2}));
else
  col = 3;
end
if n > 3
  tol = str2num(args{i+3});
else
  tol = 0.2;
end
if n > 4
  sep = args{i+4};
else
  sep = ',';
end
mi = coo - tol / 2;
ma = coo + tol / 2;
% load input data
lidar = dlmread(fname, sep);
[r, c] = size(lidar);
if c >= col
  res = find(lidar(:, col) > mi & lidar(:, col) < ma);
  printf('%.3f,%.3f,%.3f\n', [lidar(:, 1)(res), lidar(:, 2)(res), lidar(:, 3)(res)]');
  %for i = 1:r
  %  if lidar(i, col) > mi && lidar(i, col) < ma
  %    printf('%.3f,%.3f,%.3f\n', lidar(i, 1), lidar(i, 2), lidar(i, 3));
  %  end
  %end
end
