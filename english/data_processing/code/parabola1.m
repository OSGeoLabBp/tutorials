% coordinates of points
xp = [0; 21; 30]
yp = [0; 55; 75]
% set up equations
n = rows(xp);
A = [ones(n,1), xp, xp .^ 2];
l = yp;
x = A \ l
printf('Check\n')
polyval(flipud(x), xp) -yp
