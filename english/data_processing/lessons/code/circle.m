% circle fit
% x^2+y^2+a(1)*x+a(2)*y+a(3)=0
x = [ 11.88; 10.34; 2.58; -0.29 ];
y = [  0.08;  8.59; 9.54;  1.95 ];
a=[x y ones(size(x),1)]\[-(x.^2+y.^2)];
xc = -.5*a(1)
yc = -.5*a(2)
R  =  sqrt((a(1)^2+a(2)^2)/4-a(3))
% graphic representation
plot(x, y, "+r", "markersize", 10);
hold on;
xx = linspace(xc-R+0.001, xc+R-0.001, 50);
yy = sqrt(R^2 - (xx - xc).^2) +yc;
yyy = -sqrt(R^2 - (xx - xc).^2) +yc;
plot(xx, yy)
plot(xx, yyy)
