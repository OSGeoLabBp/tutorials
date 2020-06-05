format long;
if (nargin == 3)
  arg_list = argv();
  pcfile = arg_list{1};       % point cloud
  dx = str2num(arg_list{2});  % grid step
  fname = arg_list{3};        % function to use
  if (fname == "min")
    fu = @min
  elseif (fname == "max")
    fu = @max
  elseif (fname == "mean")
    fu = @mean
  elseif (fname == "median")
    fu = @median
  end
else  %just for testing
  pcfile='test32.csv'; 
  dx = 25;
  fu = @min;
end
% load point cloud and remove extra columns
points = load(pcfile)(:,1:3);
d = [dx, dx, dx];
minp = min(points, [], 1);    % get min coords
maxp = max(points, [], 1);    % get max coords
minp = floor(minp ./ d) .* d;
maxp = ceil(maxp ./d) .* d;
n = uint16((maxp .- minp) ./ d);% grid sizes
no_data = -9999.0;
% calculate row and column index to points
indexes = uint16(floor((points .- minp) ./ d)) .+ 1;
% indexes = [indexes (1:1:rows(points))']
f = fopen(strcat(pcfile, ".asc"), "w");
fprintf(f, "ncols %d\n", n(1));
fprintf(f, "nrows %d\n", n(2));
fprintf(f, "xllcorner %.3f\n", minp(1));
fprintf(f, "yllcorner %.3f\n", minp(2));
fprintf(f, "cellsize %.3f\n", d(1));
fprintf(f, "nodata_value %.3f\n", no_data);
for i = n(2):-1:1             % row from top to down
  idx = (indexes(:, 2) == i); % select points in ith row
  ii = indexes(idx, :);
  ppi = points(idx, :);
  for j = 1:n(1)
    idy = (ii(:, 1) == j);    % select points in jth cell
    ppj = ppi(idy, :);
    if (rows(ppj))
      gr = fu(ppj(:, 3));
      fprintf(f, "%.3f ", gr);
    else
      fprintf(f, "%.3f ", no_data);      
    endif
  end
  fprintf(f, "\n");
end
fclose(f);