% coordinates of points
xp = [0; 21; 30];
yp = [0; 55; 75];
% set up equations
A = zeros(3);
l = zeros(3, 1);
for i=1:3
	A(i,1) = 1;
	A(i,2) = xp(i);
	A(i,3) = xp(i)^2;
	l(i) = yp(i);
end
x = inv(A) * l
printf('Check\n')
for i=1:3    % substitute original coordinates
  A(i,:) * x - yp(i)
end
