% propagation of errors for polar observations
% formulas: y = SD * sin(Z) * sin(WCB)
%           x = SD * sin(Z) * cos(WCB)
%           z = SD * cos(Z)
% partial derivates:
%      dy/dSD = sin(Z) * sin(WCB)
%      dy/dZ  = SD * sin(WCB) * cos(Z)
%      dy/dWCB= SD * sin(Z) * cos(WCB)
%      dx/dSD = sin(Z) * cos(Z)
%      dx/dZ  = SD * cos(WCB) * cos(Z)
%      dx/dWCB=-SD * sin(Z) * sin(WCB)
%      dz/dSD = cos(Z)
%      dz/dZ  =-SD * sin(Z)
msd1 = 1.0;   % additiv tag [mm] for distance observation standard dev.
msd2 = 1.5;   % [mm/km] for distance observation standard dev.
ma = 1; % angle standard deviation [seconds]
dist = [10.0, 25.0, 50.0];   % distances to work with
z = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]; % zenith angles to work with
l = [45.0]; %  horizontal directions
zr = z .* pi / 180.0;  % change to radian
lr = l .* pi / 180.0;  % change to radian
mar = ma / (180.0 / pi * 3600.0); % change to radian
mhz = zeros(1, size(z)(2));  % initialize result vectors
mz = zeros(1, size(z)(2));
printf('dist ha za mhz mz\n');
for i = 1:size(dist)(2)
    msd = (msd1 + dist(i) / 1000.0 * msd2) / 1000.0; % in meters
    for k = 1:size(lr)(2)
        figure();
        for j = 1:size(zr)(2)
            dy_SD = sin(zr(j)) * sin(lr(k));
            dy_Z = dist(i) * sin(lr(k)) * cos(zr(j));
            dy_WCB = dist(i) * sin(zr(j)) * cos(lr(k));
            my = sqrt(dy_SD^2 * msd^2 + dy_Z^2 * mar^2 + dy_WCB^2 * mar^2);
            dx_SD = sin(zr(j)) * cos(lr(k));
            dx_Z = dist(i) * cos(lr(k)) * cos(zr(j));
            dx_WCB = -dist(i) * sin(zr(j)) * sin(lr(k));
            mx = sqrt(dx_SD^2 * msd^2 + dx_Z^2 * mar^2 + dx_WCB^2 * mar^2);
            mhz(j) = sqrt(my^2+mx^2) * 1000.0; % [mm]
            dz_SD = cos(zr(j));
            dz_Z = -dist(i) * sin(zr(j));
            mz(j) = sqrt(dz_SD^2 * msd^2 + dz_Z^2 * mar^2) * 1000.0; % [mm]
            printf('%3.0f %3.0f %3.0f %4.1f %4.1f\n', dist(i), l(k), z(j), mhz(j), mz(j));
        end
        plot(z, mz);
        hold all;
        plot(z, mhz);
        title(sprintf('Distance: %.0f Direction: %.0f', dist(i), l(k)));
        xlabel('Zenith angle [degree]');
        ylabel('Estimated error [mm]');
        legend('vertical', 'horizontal');
    end
end
