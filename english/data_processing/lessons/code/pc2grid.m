format long;
if nargin == 3
  arg_list = argv();
  pcfile = arg_list{1};       % point cloud
  dx = str2num(arg_list{2});  % grid step
  fu = arg_list{3};           % function to use
else  %just for testing
  pcfile='test32.csv'; 
  dx = 25;
  fu = "min";
end
% load point cloud and remove extra columns
points = load(pcfile)(:,1:3);
d = [dx, dx, dx];
minp = min(points, [], 1);    % get min coords
maxp = max(points, [], 1);    % get max coords
minp = floor(minp ./ d) .* d;
maxp = ceil(maxp ./d) .* d;
n = uint16((maxp .- minp) ./ d);% grid sizes
% calculate row and column index to points
indexes = uint16(floor((points .- minp) ./ d)) .+ 1;
indexes = [indexes (1:1:rows(points))']
for i = 1:n[2]
  idx = (indexes(:, 2) == i);
  ii = indexes(idx, :);
  ppi = points(idx, :);
  for j = 1:n[1]
    idy = (ii(:, 1) == j);
    ppj = ppi(idy, :);
  end
end
