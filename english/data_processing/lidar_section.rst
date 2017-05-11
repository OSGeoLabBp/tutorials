Find sections from lidar data
=============================

The task will be solved in gawk and octave, too.

Let's find first minimum and maximum values in a lidar text file to 
get the range for possible sections.
The column number is an input value.

gawk solution (*minmax.awk*)
----------------------------

.. code:: gawk

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

Let's find points at a horizontal or vertical plan (perpendicular to the axiss
of the co-ordinate system with a tolerance.

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

