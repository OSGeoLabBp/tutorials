Find sections from lidar data
=============================

*keywords*: point cloud, section

*Data file*: lidar.txt, pc_ftszv_5cm.txt

*Program files*: minmax.awk, minmax.m, minmax.py, slide.awk, slide.m, slide.py, vslide.py, np_slide.py, section.m, section_cc.py

The task will be solved in gawk, octave, Python and using command line interface of CloudCompare too.

Find min and max coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's find first minimum and maximum values in a lidar text file to 
get the range for possible sections. Any numeric column in a text file should be used.
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

Use the gawk code above like the following.

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

Python solution (minmax.py)
---------------------------

.. code:: python

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	""" find min and max values in a column of an ascii pointcloud file
		command line parameters: column_number input_file
	"""
	import sys

	if len(sys.argv) < 3:
		print("usage: {} column_number file\n".format(sys.argv[0]))
		sys.exit()
	min = 1e38
	max = -min
	col = int(sys.argv[1]) - 1  # shift column number to zero based
	with open(sys.argv[2]) as fp:
		for line in fp:
			field = float(line.strip().split(",")[col])
			if field < min: min = field 
			if field > max: max = field

	print("{:.3f} {:.3f}".format(min, max))

Sections perpendicular to an axis
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's find points close to  a horizontal or vertical plan (perpendicular to the axis
of the co-ordinate system) with a tolerance.

gawk solution (*slide.awk*)
---------------------------

.. code:: awk

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

.. note::

    The coo+0 is used to convert the string parameter to numeric value
 
.. code:: bash

    gawk -F, -f slide.awk lidar.txt > elev1000.txt
    gawk -f slide.awk -F, -v coo=1000 -v tol=0.5 -v col=3 lidar.txt > e1000.txt

Let's use GNUplot to display the section.

.. code:: gnuplot

	#!/usr/bin/gnuplot
	set xlabel "x"
	set ylabel "y"
	set grid xtics lt 1 lw 1 lc rgb "#bbbbbb"
	set grid ytics lt 1 lw 1 lc rgb "#bbbbbb"
	set autoscale
	set terminal postscript portrait enhanced mono dashed lw 1 'Helvetica' 14
	set style line 1 lt 1 lw 3 pt 3 linecolor rgb "red"
	set output 'out.eps'
	plot 'e1000.txt' using 1:2 w points title "section"

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
		./minmax.awk -F, -v col=$i $1
	done

To use the shell script above, use the following command:

.. code:: bash

	./box.sh lidar.txt
	548025.890 550424.100
	5128996.490 5129293.080
	933.310 1139.110

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

Python solution (slide.py)
-------------------------------------

In the first Pytohn solution we read the file line by line, this way there is no 
limitation for the file size.

.. code:: python

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	""" filterr point on a section perpendicular to an axis
		command line parameters: input_file, section_coordinate, column, tolerance 
	"""
	import sys

	if len(sys.argv) < 5:
		print("usage: {} file section column tolerance\n".format(sys.argv[0]))
		sys.exit()
	coo = float(sys.argv[2])
	col = int(sys.argv[3]) - 1  # shift column number to zero based
	tol = float(sys.argv[4])

	with open(sys.argv[1]) as fp:
		for line in fp:
			fields = [float(c) for c in line.strip().split(",")]
			if abs(fields[col] - coo) < tol:
				print("{:.3f},{:.3f},{:.3f}".format(fields[0], fields[1], fields[2]))

Python solution using numpy (np_slide.py)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using numpy the code becomes shorter but it uses more memory. It loads the
whole point cloud into the memory.

.. code:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    """ filter point on a section perpendicular to an axis
        command line parameters: input_file, section_coordinate, column, tolerance 
    """
    import sys
    import numpy as np

    if len(sys.argv) < 5:
        print("usage: {} file section column tolerance\n".format(sys.argv[0]))
        sys.exit()
    coo = float(sys.argv[2])
    col = int(sys.argv[3]) - 1  # shift column number to zero based
    tol = float(sys.argv[4])

    pc = np.loadtxt(sys.argv[1], delimiter=',')
    sec = pc[np.absolute(pc[:, col] - coo) < tol]
    for i in range(sec.shape[0]):
        print("{:.3f} {:.3f} {:.3f}".format(sec[i][0], sec[i][1], sec[i][2]))

Vertical section
~~~~~~~~~~~~~~~~

Python solution (vsection.py)
-----------------------------

Let's make the code more general finding the point in a vertical section.

.. code:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    """ filter points on a vertical section
        command line parameters: input_file, x1, y1, x2, y2, tolerance
        vertical plain is defined by (x1,y1) and (x2,y2)
    """
    import sys
    from math import hypot
    import numpy as np

    if len(sys.argv) < 5:
        print("usage: {} file x1 y1 x2 y2 tolerance\n".format(sys.argv[0]))
        sys.exit()
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])
    tol = float(sys.argv[6])
    # set up equation for vertical plain a * x + b * y + c = 0
    vp = np.zeros(3)
    vp[0] = y1 - y2
    vp[1] = x2 - x1
    vp[2] = x1 * y2 - x2 * y1
    # normalize
    vp = vp / hypot(vp[0], vp[1])
    mind = 1e38
    with open(sys.argv[1]) as fp:
        for line in fp:
            p = [float(c) for c in line.strip().split(",")]
            if abs(np.dot(vp, np.array([p[0], p[1], 1]))) < tol:
                print("{:.3f},{:.3f},{:.3f}".format(p[0], p[1], p[2]))

.. note::

    The section line point distance is calculated by the scalar product  of 
    the section line parameters and the homogenous coordinates (in 2D) of
    the points.

CloudCompare solution (section_cc.py)
-------------------------------------

Vertical section can be generated using CloudCompare (CC), as well. Here a simple
python script is presented to get the section using command line interface of CC.

.. code:: python

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	""" get vertical section of a point cloud using command line interface of CloudCompare
		command line parameters: input_file, e1, n1, e2, n2, tolerance
		e.g. python section_cc.py pc_ftszv_5cm.txt 660125.48 230851.85 660128.75 230835.43 0.20
	"""
	import sys
	import math
	import subprocess
	import platform

	if len(sys.argv) < 7:
		print("usage: {} file e1 n1 e2 n2 tolerance\n".format(sys.argv[0]))
		sys.exit()

	# easting and northing of 1st and 2nd points on section    
	e1 = float(sys.argv[2])
	n1 = float(sys.argv[3])
	e2 = float(sys.argv[4])
	n2 = float(sys.argv[5])
	tol = float(sys.argv[6]) 

	# coordinate differences
	de = e2 - e1
	dn = n2 - n1
	# distance
	d = math.sqrt(de**2 + dn**2)
	# sinus/cosinus of the whole circle bearing
	r = de / d
	m = dn / d

	# 1st corner of the rectangle
	ep1 = e1 - tol * m
	np1 = n1 + tol * r

	# 2nd corner of the rectangle
	ep2 = e1 + d * r - tol * m
	np2 = n1 + d * m + tol * r

	# 3rd corner of the rectangle
	ep3 = e1 + d * r + tol * m
	np3 = n1 + d * m - tol * r

	# 4th corner of the rectangle
	ep4 = e1 + tol * m
	np4 = n1 - tol * r

	# check platform
	if platform.system() is 'Windows':
	   cc="C:\Program Files\CloudCompare\CloudCompare.exe"
	elif platform.system() is 'Linux':
	   cc="cloudcompare.CloudCompare"
	else:
	   print("you can use CC on windows or linux")
	   sys.exit()

	#run CC command
	subprocess.run([cc, "-SILENT", "-O", sys.argv[1], "-C_EXPORT_FMT", "ASC", "-PREC",
        "3", "-Crop2d", "Z", "4", str(ep1), str(np1), str(ep2), str(np2), str(ep3),
        str(np3), str(ep4), str(np4)])

Another version where section points are read from a file. Output filename is also given

.. code:: python

	#!/usr/bin/env python
	# -*- coding: utf-8 -*-
	""" get vertical sections of a point cloud using command line interface of CloudCompare
	    section points are stored in a file
	    command line parameters: point_cloud_file, section_points_file, tolerance
	    e.g. python section_cc_file.py PointCloud_2020_04_30-09_27_19-15cm.ply metszetsikok.csv 0.20
	"""
	import sys
	import math
	import subprocess
	import platform
	import os
	import glob

	if len(sys.argv) < 3:
	    print("usage: {} point_cloud_file section_points_file tolerance\n".format(sys.argv[0]))
	    sys.exit()

	#point cloud filename without extension
	fname = os.path.splitext(sys.argv[1])[0]

	# check platform
	if platform.system() == 'Windows':
	    cc = "C:\Program Files\CloudCompare\CloudCompare.exe"
	    #delete all the files with the point cloud filename but with extension asc
	    fileList = glob.glob(fname + '*.asc')
	    for f in fileList:
		os.remove(f)
	elif platform.system() == 'Linux':
	    cc = "cloudcompare.CloudCompare"
	else:
	    print("you can use CC on windows or linux")
	    sys.exit()

	#print out CC command   
	#print(cc)

	#tolerance
	tol = float(sys.argv[3])

	#read section_points_file, file structure
	#station;e1;n1;e2;n2
	with open(sys.argv[2]) as fp:
	    for line in fp:
		fields = [float(c) for c in line.strip().split(";")]
		# easting and northing of 1st and 2nd points on section
		e1 = fields[1]
		n1 = fields[2]
		e2 = fields[3]
		n2 = fields[4]

		# coordinate differences
		de = e2 - e1
		dn = n2 - n1
		#distance
		d = math.hypot(de, dn)
		# sinus/cosinus of the whole circle bearing
		r = de / d
		m = dn / d

		# 1st corner of the rectangle
		ep1 = e1 - tol * m
		np1 = n1 + tol * r

		# 2nd corner of the rectangle
		ep2 = e1 + d * r - tol * m
		np2 = n1 + d * m + tol * r

		# 3rd corner of the rectangle
		ep3 = e1 + d * r + tol * m
		np3 = n1 + d * m - tol * r

		# 4th corner of the rectangle
		ep4 = e1 + tol * m
		np4 = n1 - tol * r

		#print out coordinates
		#print('{:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f} {:.3f}'.format(ep1, np1, ep2, np2, ep3, np3, ep4, np4))

		# run CC command
		subprocess.run([cc, "-SILENT", "-O", sys.argv[1], "-C_EXPORT_FMT", "ASC",
		    "-PREC", "3", "-Crop2d", "Z", "4", str(ep1), str(np1), str(ep2), str(np2),
		    str(ep3), str(np3), str(ep4), str(np4)])
		#CC automatically gives output filename
		outpf_cc = glob.glob(fname + '*.asc')
		#new filaname, first item in the section file
		outp = "{:.0f}.asc".format(fields[0])
		print(outpf_cc[0], outp)
		#delete if exists
		if os.path.exists(outp):
		    os.remove(outp)
		#rename
		os.rename(outpf_cc[0], outp)


General solution for sections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Octave solution (section.m)
---------------------------

An other general solution for sections on point cloud was made by Timea Varga 
(MSc student). It is able to filter points near to a horizontal, vertical or
general section.

.. code:: Octave

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

