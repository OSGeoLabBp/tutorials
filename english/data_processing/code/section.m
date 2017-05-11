% Section of a point cloud
% (c)Varga Timea, Siki Zoltan 2017
% 
% commandline parameters:
%   txt_point_cloud - path to the point cloud file
%   section_type - 1/2/3 horizontal/vertical/general section
%   for horizontal section:
%     elevation - section elevation
%     tolerance - tolerace for section
%     output_file - name of output file
%   for vertical section:
%     x1 y1 - first point on section
%     x2 y2 - second point onsection
%     tolerance - tolerace for section
%     output_file - name of output file
%   for general section:
%     x1 y1 z1 - first point on section plane
%     x2 y2 z2 - second point on section plane
%     x3 y3 z3 - third point on section plane
%     tolerance - tolerace for section
%     output_file - name of output file
version = 1.0;

function [xh, yh, zh] = h_sec(x, y, z, height, tol)
%  creating horizontal section
  res = find(z >= height-tol & z <= height+tol);
  xh = x(res);
  yh = y(res);
  zh = z(res);
end

args = argv();
n = rows(args);
i = 1
if n > 0
  while i <= rows(args) && args{i}(1) == '-'
    i += 1
    n -= 1
  end
end
if n > 0
  fname = args{i};
else
  fname = '03_10.txt';
end
ptCloud = load(fname);
x = ptCloud (:,1);
y = ptCloud (:,2);
z = ptCloud (:,3);

% section type selection
if n > 1
  section = str2num(args{i+1});
else
  section = input('Horizontal section - 1, Vertical section - 2, General section - 3: ');
end
if section == 1
  % horizontal section
  if n > 2
    height = str2num(args{i+2});
  else 
    height = input(sprintf('Section height[m] (%.3f-%.3f):', min(z), max(z))); % elevation for section
  end
  if isempty(height)
    height = mean(z); % default elevation
  end
  if n > 3
    tol = str2num(args{i+3});
  else    
    tol = input('Tolerance[m]:');
  end
  if isempty(tol)
    tol = 0.05; % default tolerance 5 cm
  end
%  creating horizontal section
  [xh, yh, zh] = h_sec(x, y, z, height, tol);
  if n > 4
    % output section data
    fp = fopen(args{i+4}, 'w');
    fprintf(fp, '%.3f %.3f %.3f\n', [xh, yh, zh]');
    fclose(fp);
  else
    % show section
    figure(2); clf;
    plot (xh,yh, 'rx')
    axis equal
    title('Horizontal section')  
  end
% vertical section
elseif section == 2
  if n > 5
    p1x = str2num(args{i+2});
    p1y = str2num(args{i+3});
    p2x = str2num(args{i+4});
    p2y = str2num(args{i+5});
  else
    % horizontal section for graphical input
    [xh, yh, zh] = h_sec(x, y, z, mean(z), 0.05);
    % select section points on horizontal section
    figure(2)
    plot (xh,yh, 'rx')
    axis equal
    title('Select the first point')
    [p1x,p1y] = ginput(1); % first point of section

    figure (2)
    title('Select the second point')
    [p2x,p2y] = ginput(1); % second point of section
  end
  if n > 6
    tol = str2num(args{i+6});
  else    
    tol = input('Tolerance[m]:');
  end
  if isempty(tol)
    tol = 0.05; % default tolerace 5cm
  end
   
  p1 = [p1x p1y];
  p2 = [p2x p2y];

  normal = [p2y - p1y; p1x - p2x]; % normal vector
  normal = normal ./ norm(normal, 2); % normalization
  a = normal(1); 
  b = normal(2);
  d = -p1 * normal; % coeff

  dist = find(abs((a*x+b*y+d)) <= tol); % distance from vertical plane

  xv = x(dist);
  yv = y(dist);
  zv = z(dist);

  if n > 7
    % output section data
    fp = fopen(args{i+7}, 'w');
    fprintf(fp, '%.3f %.3f %.3f\n', [xv, yv, zv]');
    fclose(fp);
  else
    % display section
    figure(3);clf;
    axis equal;
    plot3(xv,yv,zv,'rx')
    title('Vertical section')
  end

% general section
elseif section == 3
args
  if n > 10
    p1x = str2num(args{i+2});
    p1y = str2num(args{i+3});
    p1z = str2num(args{i+4});
    p2x = str2num(args{i+5});
    p2y = str2num(args{i+6});
    p2z = str2num(args{i+7});
    p3x = str2num(args{i+8});
    p3y = str2num(args{i+9});
    p3z = str2num(args{i+10});
  else
    % horizontal section for imput
    [xh, yh, zh] = h_sec(x, y, z, mean(z), 0.05);
    
    % selecting points on horizontal section
    figure(2)
    plot (xh,yh, 'rx')
    axis equal
    title('Select the first point')
    [p1x,p1y] = ginput(1);
    p1z = input(sprintf('Height of point[m] (%.3f-%.3f):', min(z), max(z)));

    figure (2)
    title('Select the second point')
    [p2x,p2y] = ginput(1);
    p2z = input(sprintf('Height of point[m] (%.3f-%.3f):', min(z), max(z)));
    
    figure (2)
    title('Select the third point')
    [p3x,p3y] = ginput(1);
    p3z = input(sprintf('Height of point[m] (%.3f-%.3f):', min(z), max(z)));
  end    
  if n > 11
    tol = str2num(args{i+11});
  else    
    tol = input('Tolerance[m]:');
  end
  if isempty(tol)
    tol = 0.05; % default tolerace 5cm
  end
  p1 = [p1x p1y p1z];
  p2 = [p2x p2y p2z];
  p3 = [p3x p3y p3z];
  normal = cross(p1 - p2, p1 - p3); % normalvektor
  normal = normal ./ norm(normal, 2); % normalizalas
  a = normal(1); 
  b = normal(2);
  c = normal(3);
  d = -p1 * normal'; % coeff
    
  dist = find(abs((a*x+b*y+c*z+d)) <= tol); % distance from plane
    
  xg = x(dist);
  yg = y(dist);
  zg = z(dist);
  
  if n > 12
    % output section data
    fp = fopen(args{i+12}, 'w');
    fprintf(fp, '%.3f %.3f %.3f\n', [xg, yg, zg]');
    fclose(fp);
  else  
    % display result
    figure(4);clf;
    axis equal;
    plot3(xg,yg,zg,'rx')
    title('General section')   
  end
end
