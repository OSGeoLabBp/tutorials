Find sections from lidar data
=============================

The task will be solved in gawk and octave, too.

Let's find first minimum and maximum values in a lidar text file to 
get the range for possible sections.
The column number is an input value.

gawk solution (*minmax.awk*)
----------------------------

.. code:: gawk

	#! /usr/bin/gawk -f
    # find minimal and maximal values in a column
    # column number can be set from command line: -v col=2
    BEGIN { mi = 1e10; ma = -1e10;
      if (col+0 == 0) { col = 1; }  # is col defined?
    }
    { if (NF >= col) {
        if ($col < mi) { mi = $col; }
        if ($col > ma) { ma = $col; }
      }
    } 
    END { printf("%.3f %.3f\n", mi, ma; }

.. code:: bash

	gawk -F, -v col=3 -f minmax.awk lidar.txt
	933.31 1139.11

.. note::

	The first line called shebang, it is useful on Linux if you make the
	gawk program file executable (e.g. chmod +x minmax.awk).
	To run the program input: ./minmax.awk -F, -v col=3 lidar.txt

octave solution (minmax.m)
--------------------------

.. code:: octave

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

Example of running in a terminal:

.. code:: bash

	octave -qf minmax.m 1.txt 2 " "

Let's find the 3D bounding box of the pointcloud calling minmax.awk three times
from a shell script.

.. code:: bash

	#! /bin/bash
	if [ $# -ne 1 ]
	then
		echo "usage? $0 <file>"
		exit 1
	fi
	if [ ! -f $1 ]
	then
		echo "$1 file not found"
		exit 2
	fi
	for i in {1..3}
	do
		./minmax.awk -v col=$i $1
	done


Let's find points at a horizontal or vertical plan (perpendicular to the axis
of the co-ordinate system) with a tolerance.

gawk solution (*slide.awk*)
---------------------------

.. code::

	# get a slide from point cloud perpendicular to one of the axis
	# of the co-ordinate system with a tolerance
	# parameters
	#   coo - fix coordinate for slide
	#   col - column to test from input file
	#   tol - tolerance
    BEGIN { if (coo+0 == 0) { coo = 1000; } # check input variables
            if (tol+0 == 0) { tol = 0.2; }
            if (col+0 == 0) { col = 3; }
            mi = coo - tol / 2; # range of coordinates in section
            ma = coo + tol / 2;
    }
    {  if (NF >= col) {
            if ($col > mi && $col < ma) { print $0; }
       }
    }
 
.. code::

    gawk -F, -f slide.awk lidar.txt > elev1000.txt
    gawk -f slide.awk -F, -v coo=1000 -v tol=0.5 -v col=3 lidar.txt > e1000.txt

octave solution (slide.m)
-------------------------

.. code:: octave

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
	  sep = args{5};
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
	end

The Octave solution above does not work for huge files as the whole file is
processed in memory. Let's rewrite the code to process huge files in
chunks (*slide1.m*).

.. code:: octave

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
	% load data in chunks
	f = fopen(fname);
	form = ['%f' sep '%f' sep '%f'];
	chunk = 65000;
	while (1)
		lidar = fscanf(f, form, [3, chunk])';
		[r, c] = size(lidar);
		if r < 2 || c < 2
			break;
		end
		if c >= col
		    i = find(lidar(:, col) > mi & lidar(:, col) < ma);
			printf('%.3f,%.3f,%.3f\n', lidar(i, 1:3)');
		end
	end

General solution for sections (section.m)
-----------------------------------------

An other general solution for sections on point cloud was made by Timea Varga 
(MSc student). It is able to filter points near to a horizontal, vertical or
general section.

.. code::


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
