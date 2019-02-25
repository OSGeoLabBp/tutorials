% circle fit coordinate file
% read data from ascii file
args = argv();
if rows(args) == 0
	fname = 'circletest.txt';
else
	fname = args{1};
end
points = dlmread(fname);
a=[points(:,1) points(:,2) ones(rows(points),1)]\[-(points(:,1).^2+points(:,2).^2)];
xc = -.5*a(1)
yc = -.5*a(2)
R  =  sqrt((a(1)^2+a(2)^2)/4-a(3))
