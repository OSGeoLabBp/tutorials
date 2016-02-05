% LiDAR data processing
 % load input data
 load lidar.txt;
 % data stored in array 'lidar' same as lidar = dlmread('lidar.txt', ',');
 % set window for processing
 xmin = 548040;
 ymin = 5129010;
 xmax = 548300;
 ymax = 5129270;
 dx = 10;    % GRID step
 dy = 10;
 % generate x & y grid
[x, y] = meshgrid(xmin:dx:xmax, ymin:dy:ymax);
 % grid interpolation for z
 z = griddata(lidar(:,1), lidar(:,2), lidar(:,3), x, y, 'linear');
 figure();    % 3D surface plot
 mesh(x, y, z);    % display mesh in 3D
 title('3D GRID');
 figure();
 meshc(x, y, z);   % display contours
 title('3D GRID and Contours');
 % contour lines
 figure(); contour(x, y, z);
 title('Contours');
 % volume calculation above 1000 m
 vol = 0;
 [r, c] = size(z);
 for ir = 1:r
     for ic = 1:c
         p = z(ir, ic);
         if (p > 1000)
             vol += dx * dy * (p - 1000);
         end
     end
 end
 printf('Volume above 1000m: %.0f m3\n', vol);
 % vectorized solution for volume calculation
 vol1 = sum(z(z > 1000) - 1000) * dx * dy;
 printf('Volume above 1000m: %.0f m3 (vectorized)\n', vol1);
