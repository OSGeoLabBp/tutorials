#! /usr/bin/octave -qf
format long;
% process command line arguments
if (nargin > 0)
  arg_list = argv();
  pcfile = arg_list{1};       % point cloud
  if (nargin > 1)
    dx = str2num(arg_list{2});  % grid step
  else
    dx = 1;                   % default cell size
  end
  if (nargin > 2)
    fname = arg_list{3};        % function to use
  else
    fname = "min";
  end
  if (strncmp(fname, "min", 2))
    fu = @min;
  elseif (strncmp(fname, "max", 2))
    fu = @max;
  elseif (strncmp(fname, "mean", 3))
    fu = @mean;
  elseif (strncmp(fname, "median", 3))
    fu = @median;
  elseif (strncmp(fname, "numel", 2))
    fu = @numel;
  end
else
  printf("Usage pc2grid.m point_cloud_file [resolution] [min/max/mean/median/num]\n");
  exit(1)
end
no_data = -9999.0;
start_time = time();
% load point cloud and remove extra columns
points = load(pcfile)(:,1:3);
printf("--- reading %.2f seconds ---\n", time() - start_time);
start_time1 = time();
d = [dx, dx, dx];
minp = min(points, [], 1);    % get min coords
maxp = max(points, [], 1);    % get max coords
minp = floor(minp ./ d) .* d;
maxp = ceil(maxp ./d) .* d;
n = uint32((maxp .- minp) ./ d);% grid sizes
% calculate row and column index to points
indexes = uint32(floor((points .- minp) ./ d)) .+ 1;
indexes = [indexes (1:1:rows(points))'];
printf("--- indexing %.2f seconds ---\n", time() - start_time1);
% create grid selecting point in cells
% headers for grid file
start_time2 = time();
f = fopen(strcat(pcfile, ".asc"), "w");
fprintf(f, "ncols %d\n", n(1));
fprintf(f, "nrows %d\n", n(2));
fprintf(f, "xllcorner %.3f\n", minp(1));
fprintf(f, "yllcorner %.3f\n", minp(2));
fprintf(f, "cellsize %.3f\n", d(1));
fprintf(f, "nodata_value %.3f\n", no_data);
for i = n(2):-1:1             % rows from top to down
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
    end
  end
  fprintf(f, "\n");
end
fclose(f);
printf("--- griding1 %.2f seconds ---\n", time() - start_time2);
% create grid sorting points by bucket indices
sorted_indexes = sortrows(indexes, [-2, 1]);
start_time3 = time();
% headers for grid file
f = fopen(strcat(pcfile, "_1.asc"), "w");
fprintf(f, "ncols %d\n", n(1));
fprintf(f, "nrows %d\n", n(2));
fprintf(f, "xllcorner %.3f\n", minp(1));
fprintf(f, "yllcorner %.3f\n", minp(2));
fprintf(f, "cellsize %.3f\n", d(1));
fprintf(f, "nodata_value %.3f\n", no_data);
% buffer for a row of grid
grid = ones(n(1), 1) * no_data;
i = sorted_indexes(1,2);
j = sorted_indexes(1,1);
start = 1;
m = rows(sorted_indexes);
for k = 1:m
  % grid distance in row order of cells
  gd = (i - sorted_indexes(k, 2)) * n(1) + sorted_indexes(k, 1) - j;
  if gd
    grid(j) = fu(points(sorted_indexes(start:k-1, 4), 3));
    for ii = sorted_indexes(k, 2):i-1
      for jj = 1:n(1)
          fprintf(f, "%.3f ", grid(jj));
      end
      fprintf(f, "\n");  
      grid = ones(n(1), 1) * no_data;    
    end
    j = sorted_indexes(k,1);
    i = sorted_indexes(k, 2);
    start = k;
  end
end
% set last bucket
grid(j) = fu(points(sorted_indexes(start:m, 4), 3));
for jj = 1:n(1)
  fprintf(f, "%.3f ", grid(jj));
end
fprintf(f, "\n");  
fclose(f);
printf("--- griding2 %.2f seconds ---\n", time() - start_time3);
% collect points in the same cell
start_time4 = time();
% headers for grid file
f = fopen(strcat(pcfile, "_2.asc"), "w");
fprintf(f, "ncols %d\n", n(1));
fprintf(f, "nrows %d\n", n(2));
fprintf(f, "xllcorner %.3f\n", minp(1));
fprintf(f, "yllcorner %.3f\n", minp(2));
fprintf(f, "cellsize %.3f\n", d(1));
fprintf(f, "nodata_value %.3f\n", no_data);
grid = cell(n(2),n(1));
for k = 1:m
  grid{indexes(k, 2), indexes(k, 1)} = [grid{indexes(k,2), indexes(k, 1)}, points(k, 3)];
end
for i = n(2):-1:1             % rows from top to down
  for j = 1:n(1)
    if columns(grid{i, j})
      fprintf(f, "%.3f ", fu(grid{i, j}));
    else
      fprintf(f, "%.3f ", no_data);
    end
  end
  fprintf(f, "\n");
end
printf("--- griding3 %.2f seconds ---\n", time() - start_time4);
