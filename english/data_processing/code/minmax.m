% find minimal and maximal values in a column
% column number can be set from command line
% parameters:
%   fname - input coordinate file (default lidar.txt)
%   col - coordinate column (default 3)
%   sep - separator in input file (default ',')
args = argv();  % command line arguments in a cell array
 % check positional parameters
if nargin > 0
  fname = args{1};
else
  fname = 'lidar.txt';
end
if nargin > 1
  col = int32(str2num(args{2}));
else
  col = 3;
end
if nargin > 2
  sep = args{3};
else
  sep = ',';
end
% load input data
lidar = dlmread(fname, sep);
printf('%.3f %.3f\n', min(lidar(:, col)), max(lidar(:, col)));