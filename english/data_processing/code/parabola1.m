% coordinates of points
xp = [0; 21; 30];
yp = [0; 55; 75];
% set up equations
A = zeros(3, 3);
l = zeros(3, 1);
A(:,1) = ones();
A(:,2) = xp;
A(:,3) = xp.^2;
l = yp;
x = A \ l
printf('Check\n')
polyval(flipud(x), xp) -yp
