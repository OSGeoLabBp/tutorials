Level network adjustment and data snooping
==========================================

*Keywords*: matrix operations, formatted output, vectorization

*Data file*: None

*Program file*: adjust.m, adjust1.m


*Octave solution*:

First version with loops (adjust.m)

.. code:: octave

    % sample calculation of a level network ajustment
    % (c) Zoltan Siki 2012-2014 siki.zoltan at epito.bme.hu
    % point numbers are the ordinal number for simplicity
    % 1 o------o 2
    %   |\    /|
    %   | \  / |
    %   |  \/  |
    %   |  /\  |
    %   | /  \ |
    %   |/    \|
    % 4 o------o 3
    % a priori standard deviation of unit weight is 1
    % usage: octave /path_to_file/mkiegy.m
    format long
    % --------- start of editable part ---------------------------------------
    % standard deviation of leveling [mm/km]
    mkm = 0.7;
    psz = [1, 2, 3, 4];   % point numbers
    % prelimenary/final elevations 1,2,3,4
    mag = [104.234; 103.487; 102.958; 101.345];  %preliminary coordinates
    % number of unknowns (at the beginning of point numbers)
    n = 3;
    % observations: start  end height_difference length
    %               index index  [m]              [km]
    dm = [            1,    2,   -0.749,          1.1;
                      1,    3,   -1.274,          1.8;
                      1,    4,   -2.890,          1.4;
                      2,    3,   -0.530,          1.5;
                      2,    4,   -2.141,          1.9;
                      3,    4,   -1.614,          0.9 ];
    % --------- end of editable part -----------------------------------------
    if (n > length(mag) || n <= 0)
        n = length(mag);    % all points are unknown
    end
    m = length(dm(:,1));    % number of equations
    A = zeros(m, n);        % initialization of coefficient matrix (m x n)
    P = zeros(m, m);        % initialization of weight matrix (m x m)
    l = zeros(m, 1);        % initialization of pure terms
    for i = 1:m             % set up matrices
        if (dm(i,1) <= n)
            A(i, dm(i, 1)) = -1;
        end
        if (dm(i,2) <= n)
            A(i, dm(i, 2)) = 1;
        end
        P(i, i) = 1 / (dm(i, 4) * mkm)^2; % [mm^-2]
        l(i) = -((mag(dm(i, 2)) - mag(dm(i, 1))) - dm(i, 3)) * 1000; % [mm]
    end
    N = A' * P * A;
    if (n > rank(N))    % singular matrix?
        Ninv = pinv(N);
    else
        Ninv = inv(N);
    end
    f = m - rank(N);        % number of redundant observations
    x = Ninv * A' * P * l;  % change of preliminary values [mm]
    v = A * x - l;          % corrections [mm]
    X = mag(1:n) .+ (x / 1000); % adjusted elevations
    m0 = sqrt((v' * P * v) / f); % standard deviation of unit weight
    mz = m0 * sqrt(diag(Ninv));  % standard deviation of elevations
    U = dm(:, 3) .+ (v / 1000);  % adjusted observations [m]
    %Qll = inv(P);               % variance/covariance matrix
    Qll = zeros(m,m);
    for i=1:m
        Qll(i,i) = 1 / P(i,i);
    end
    Quu = A * Ninv * A'; % a posteriori variance/covariance of observations
    mu = m0 * sqrt(diag(Quu)); % standard deviations of height differences
    Qvv = Qll - Quu; % variance/covariance matrix of corrections
    s = zeros(m,1); % statistics for probe
    sn = zeros(m,1);
    r = zeros(m,1);
    for i = 1:m
        s(i) = abs(v(i)) / (m0 * sqrt(Qvv(i,i)));
        % t distribution
        sn(i) = abs(v(i)) / sqrt(Qvv(i,i));
        % normal distribution
        r(i) = 1 - Quu(i,i) * P(i,i);
    end
    % check for calculation w1 == w2?
    w1 = v' * P * v;
    w2 = -l' * P * v;
    % output results
    printf('--------------------------------------------\n');
    printf('Point Preliminary Elevation Adjusted Std.dev\n')
    printf('       elevation   change  elevation\n')
    printf('          [m]       [mm]       [m]     [mm]\n')
    printf('--------------------------------------------\n')
    for i = 1:n
        printf('%3d %8.4f %8.4f %8.4f %6.2f\n', psz(i), mag(i), x(i), X(i), mz(i))
    end
    for i = n+1:length(mag)
        printf('%3d %8.4f\n', psz(i), mag(i));
    end
    printf('---------------------------------------------------------\n')
    printf(' Sp Ep Obs. Cor. Adjust.  StDev. Stat. Stat.  r\n')
    printf('       [m]  [mm]   [m]     [mm]    t     U\n')
    printf('---------------------------------------------------------\n')
    for i = 1:m
        printf('%3d %3d %7.4f %5.2f %7.4f %8.2f %5.1f %5.1f %5.1f\n', ...
        psz(dm(i, 1)), psz(dm(i, 2)), dm(i, 3), v(i), U(i), ...
        mu(i), s(i), sn(i), r(i))
    end
    printf('---------------------------------------------------------\n\n')
    printf('m0 = %5.2f\n', m0)
    printf('Check: %8.3f = %8.3f\n', w1, w2)


*Results*:

.. code:: text

    --------------------------------------------
    Point Preliminary Elevation Adjusted Std.dev
           elevation   change  elevation
              [m]       [mm]       [m]     [mm]
    --------------------------------------------
      1    104.2340    0.9969   104.2350   1.13
      2    103.4870   -0.1919   103.4868   1.19
      3    102.9580    0.8200   102.9588   0.91
      4    101.3450
    ------------------------------------------------------
     Sp  Ep    Obs.  Cor.  Adjust.  StDev. Stat. Stat.  r
               [m]   [mm]    [m]     [mm]    t    U
    ------------------------------------------------------
      1   2 -0.7490  0.81 -0.7482   1.06   1.1   1.9   0.3
      1   3 -1.2740 -2.18 -1.2762   1.17   1.3   2.1   0.7
      1   4 -2.8900  0.00 -2.8900   1.13   0.0   0.0   0.5
      2   3 -0.5300  2.01 -0.5280   1.17   1.6   2.6   0.5
      2   4 -2.1410 -0.81 -2.1418   1.19   0.4   0.7   0.7
      3   4 -1.6140  0.18 -1.6138   0.91   0.4   0.6   0.2
    ------------------------------------------------------

    m0 =  1.65
    Check:    8.217 =    8.217

Second, vectorized version (adjust1.m)

.. code:: octave

	% sample calculation of a level network ajustment
	% vectorized version
	% (c) Zoltan Siki 2019 siki.zoltan at epito.bme.hu
	% point numbers are the ordinal number for simplicity
	% 1 o------o 2
	%   |\    /|
	%   | \  / |
	%   |  \/  |
	%   |  /\  |
	%   | /  \ |
	%   |/    \|
	% 4 o------o 3
	% a priori standard deviation of unit weight is 1
	% usage: octave /path_to_file/mkiegy.m
	format long
	% --------- start of editable part ---------------------------------------
	% standard deviation of leveling [mm/km]
	mkm = 0.7;
	psz = [1, 2, 3, 4];   % point numbers
	mag = [104.234; 103.487; 102.958; 101.345];  %preliminary elevations
	% number of unknowns (from the beginning of point numbers)
	n = 3;
	% observations: start  end height_difference length
	%               index index  [m]              [km]
	dm = [            1,    2,   -0.749,          1.1;
					  1,    3,   -1.274,          1.8;
					  1,    4,   -2.890,          1.4;
					  2,    3,   -0.530,          1.5;
					  2,    4,   -2.141,          1.9;
					  3,    4,   -1.614,          0.9 ];
	% --------- end of editable part -----------------------------------------
	if (n > length(mag) || n <= 0)
		n = length(mag);    % all points are unknown
	end
	m = length(dm(:,1));    % number of equations
	A = zeros(m, n);        % initialization of coefficient matrix (m x n)
	P = zeros(m, m);        % initialization of weight matrix (m x m)
	l = zeros(m, 1);        % initialization of pure terms
	for i = 1:m             % set up matrices
		if (dm(i,1) <= n)
			A(i, dm(i, 1)) = -1;
		end
		if (dm(i,2) <= n)
			A(i, dm(i, 2)) = 1;
		end
	end
	P(1:1+size(P,1):end) = 1.0 ./ (dm(:, 4) .* mkm).^2      % wights
	l = -(mag(dm(:,2)) .- mag(dm(:,1)) - dm(:,3)) * 1000.0; % pure terms
	N = A' * P * A;
	if (n > rank(N))    % singular matrix?
		Ninv = pinv(N);
	else
		Ninv = inv(N);
	end
	f = m - rank(N);        % number of redundant observations
	x = Ninv * A' * P * l;  % change of preliminary values [mm]
	v = A * x - l;          % corrections [mm]
	X = mag(1:n) .+ (x / 1000); % adjusted elevations
	m0 = sqrt((v' * P * v) / f); % standard deviation of unit weight
	mz = m0 * sqrt(diag(Ninv));  % standard deviation of elevations
	U = dm(:, 3) .+ (v / 1000);  % adjusted observations [m]
	%Qll = inv(P);               % variance/covariance matrix
	Qll = zeros(m,m);
	Qll(1:1+size(Qll,1):end) = 1.0 ./ diag(P)
	Quu = A * Ninv * A'; % a posteriori variance/covariance of observations
	mu = m0 * sqrt(diag(Quu)); % standard deviations of height differences
	Qvv = Qll - Quu; % variance/covariance matrix of corrections
	s = abs(v) ./ (m0 * sqrt(diag(Qvv)));	% statistics for t probe
	sn = abs(v) ./ sqrt(diag(Qvv));			% statistics for U probe
	r = 1 - diag(Quu) .* diag(P);			% relative redundant observations
	% check for calculation w1 == w2?
	w1 = v' * P * v;
	w2 = -l' * P * v;
	% output results
	printf('--------------------------------------------\n');
	printf('Point Preliminary Elevation Adjusted Std.dev\n')
	printf('       elevation   change  elevation\n')
	printf('          [m]       [mm]       [m]     [mm]\n')
	printf('--------------------------------------------\n')
	for i = 1:n
		printf('%3d    %8.4f  %8.4f   %8.4f %6.2f\n', psz(i), mag(i), x(i), X(i), mz(i))
	end
	for i = n+1:length(mag)
		printf('%3d    %8.4f\n', psz(i), mag(i));
	end
	printf('------------------------------------------------------\n')
	printf(' Sp  Ep    Obs.  Cor.  Adjust.  StDev. Stat. Stat.  r\n')
	printf('           [m]   [mm]    [m]     [mm]    t    U\n')
	printf('------------------------------------------------------\n')
	for i = 1:m
		printf('%3d %3d %7.4f %5.2f %7.4f %6.2f %5.1f %5.1f %5.1f\n', ...
		psz(dm(i, 1)), psz(dm(i, 2)), dm(i, 3), v(i), U(i), ...
		mu(i), s(i), sn(i), r(i))
	end
	printf('------------------------------------------------------\n\n')
	printf('m0 = %5.2f\n', m0)
	printf('Check: %8.3f = %8.3f\n', w1, w2)

Python/numpy  solution

.. code:: python

	import math
	import numpy as np

	mkm = 0.7
	psz = np.array([1, 2, 3, 4])  # point numbers
	mag = np.array([104.234, 103.487, 102.958, 101.345]) # elevations
	n = 3   # number of unknown from the beginning of point numbers
	# observations: start  end height_difference length
	#               index index  [m]              [km]
	dm = np.array([[0,    1,   -0.749,          1.1],
				   [0,    2,   -1.274,          1.8],
				   [0,    3,   -2.890,          1.4],
				   [1,    2,   -0.530,          1.5],
				   [1,    3,   -2.141,          1.9],
				   [2,    3,   -1.614,          0.9 ]])
	# --------- end of editable part -----------------------------------------
	if n > mag.size or n <= 0:
		n = mag.size
	m = dm.shape[0] # number of equations
	A = np.zeros((m, n))
	P = np.zeros((m, m))
	l = np.zeros((m, ))
	for i in range(m):
		if dm[i,0] < n:
			A[i, int(dm[i,0])] = -1
		if dm[i,1] < n:
			A[i, int(dm[i,1])] = 1
		P[i,i] = 1.0 / (dm[i,3] * mkm)**2
		l[i] = -((mag[int(dm[i,1])] - mag[int(dm[i,0])]) - dm[i,2]) * 1000
	N = A.transpose().dot(P).dot(A)
	r = np.linalg.matrix_rank(N)
	if n > r:
		Ninv = np.linalg.pinv(N)
	else:
		Ninv = np.linalg.inv(N)
	f = m - r   # nunmber of redundant observations
	x = Ninv.dot(A.transpose()).dot(P).dot(l)
	v = A.dot(x) - l            # corrections [mm]
	X = mag[:n] + (x / 1000.0)  # adjusted elevations
	m0 = math.sqrt(v.transpose().dot(P).dot(v) / f)
	mz = m0 * np.sqrt(np.diag(Ninv))
	U = dm[:,2] + (v / 1000.0)  # adjusted observations
	Qll = np.zeros((m, m))
	for i in range(m):
		Qll[i,i] = 1 / P[i,i]
	Quu = A.dot(Ninv).dot(A.transpose())
	mu = m0 * np.sqrt(np.diag(Quu))
	Qvv = Qll - Quu
	s = np.zeros(m)             # statistics for blunder
	sn = np.zeros(m)
	r = np.zeros(m)
	for i in range(m):
		s[i] = abs(v[i]) / (m0 * math.sqrt(Qvv[i,i]))
		sn[i] = abs(v[i]) / math.sqrt(Qvv[i,i])
		r[i] = 1.0 - Quu[i,i] * P[i,i]
	# check for calculation
	w1 = v.transpose().dot(P).dot(v)
	w2 = -l.transpose().dot(P).dot(v)
	print('--------------------------------------------');
	print('Point Preliminary Elevation Adjusted Std.dev')
	print('       elevation   change  elevation')
	print('          [m]       [mm]       [m]     [mm]')
	print('--------------------------------------------')
	for i in range(n):
		print('{:3d}    {:8.4f}  {:8.4f}   {:8.4f} {:6.2f}'.format(psz[i], mag[i], x[i], X[i], mz[i]))
	for i in range(n, len(mag)):
		print('{:3d}    {:8.4f}'.format(psz[i], mag[i]))
	print('------------------------------------------------------')
	print(' Sp  Ep    Obs.  Cor.  Adjust.  StDev. Stat. Stat.  r')
	print('           [m]   [mm]    [m]     [mm]    t    U\n')
	print('------------------------------------------------------')
	for i in range(m):
		print('{:3d} {:3d} {:7.4f} {:5.2f} {:7.4f} {:6.2f} {:5.1f} {:5.1f} {:5.1f}'.format(psz[int(dm[i, 0])], psz[int(dm[i, 1])], dm[i, 2], v[i], U[i], mu[i], s[i], sn[i], r[i]))
	print('------------------------------------------------------')
	print('m0 = {:5.2f}'.format(m0))
	print('Check: {:8.3f} = {:8.3f}'.format(w1, w2))

.. note:: 

	If you need more complex processing of geodetic networks use 
	`GNU Gama <https://www.gnu.org/software/gama>` and
	`GeoEasy <https://github.com/zsiki/GeoEasy>`, both are open source.

.. note:: *Developing tipps*:

    Input from file, Automatic blunder detection and removal.
	More vectorization, more compact code.
