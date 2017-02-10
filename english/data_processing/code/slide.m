% get a slide from point cloud perpendicular to one of the axis
% of the co-ordinate system with a tolerance
% parameters:
%   fname - input coordinate file (default lidar.txt)
%   coo - coordinate of section (default 1000)
%   col - coordinate column (default 3)
%   tol - tolerance to co-ordinate (default 0.2)
%   sep - separator in input file (default ',')
args = argv();  % command line arguments in a cell array
 % check positional parameters
if nargin > 0
  fname = args{1};
else
  fname = 'lidar.txt';
end
if nargin > 1
  coo = str2num(args{2});
else
  coo = 1000;
end
if nargin > 2
  col = int32(str2num(args{3}));
else
  col = 3;
end
if nargin > 3
  tol = str2num(args{4});
else
  tol = 0.2;
end
if nargin > 4
  sep = args{4};
else
  sep = ',';
end
mi = coo - tol / 2;
ma = coo + tol / 2;
% load input data
lidar = dlmread(fname, sep);
[r, c] = size(lidar);
if c >= col
  for i = 1:r
    if lidar(i, col) > mi && lidar(i, col) < ma
      printf('%.3f,%.3f,%.3f\n', lidar(i, 1), lidar(i, 2), lidar(i, 3));
    end
  end
end
