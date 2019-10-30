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
