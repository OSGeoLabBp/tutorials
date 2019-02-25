#!/usr/bin/octave
args = argv();    % command line arguments
% load all coordinates
if (length(args))
    fp = fopen(args{1}, 'r');
else
    fp = fopen('monitoring.csv', 'r');
end
% read data in goups of ten values, nn total number of items read
[points, nn]=fscanf(fp, '%d;%f;%f;%f;%d-%d-%d %d:%d:%d', [10, Inf]);
fclose(fp);
points = points';    % transpose
n=numel(points(:,1));  % number of rows
% different point numbers
pnums=sortrows(unique(points(:,1)));
% number of points
npnums=numel(pnums);
% change time to seconds
points(:,5)=points(:,8)*3600+points(:,9)*60+points(:,10);
% graph for time - Z
% point series
point_serie=sortrows(points,1);
% set up intervalts by point numbers
i1 = zeros(npnums);
i2 = zeros(npnums);
actp = pnums(1);
j = 1;
i1(j) = 1;
for i = 2:n
    if (actp ~= point_serie(i,1))
        % point number changed
        i2(j) = i - 1;
        j++;
        i1(j) = i;
        actp = point_serie(i,1);
    end
end
i2(npnums) = n;
for i = 1:14 %npnums-1
    plot(point_serie(i1(i):i2(i),5),point_serie(i1(i):i2(i),4));
    hold all
end
title('time - Z');
xlabel('time [sec]');
ylabel('Z [m]');
% save figure to file
saveas(1, 'img1.png');
% cleate legend labels, point numbers as string
legend(strsplit(strtrim(sprintf('%d ', pnums(1:14))), ' '))
