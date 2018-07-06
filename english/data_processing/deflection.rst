Processing bridge deflection data
=================================

*Keywords*: monitoring, GNSS, total station, time series

*Data files*: gnss.txt, totalstation.txt

*Program files*: gnss_totals.m

Birdge deflections were observed at a point by GNSS and total station 
second by second.
The change of the elevations are compared and examined. Cross correlation is
calculated between the two data series to find time offset.
Finally some statistical values are calculated.

.. code:: octave

	% gnss & totalstation
	pkg load signal
	format long
	% -----------------------------------------------------
	% load gnss data from file
	fin = fopen('gnss.txt');
	log = fscanf(fin, '%f %f %f %d:%d:%d', [6 inf])';
	fclose(fin);
	% change H:M:S to secs
	t_gnss = log(:,4) * 3600 + log(:,5) * 60 + log(:,6);
	h_gnss = log(:,3);
	% -----------------------------------------------------
	% load ts data from file
	fin = fopen('totalstation.txt');
	log = fscanf(fin, '%f %f %f %d:%d:%d', [6 inf])';
	fclose(fin);
	% change H:M:S to secs
	t_ts = log(:,4) * 3600 + log(:,5) * 60 + log(:,6);
	h_ts = log(:,3);
	% -----------------------------------------------------
	% common part dropping first/last 30 seconds
	t_start = max(t_gnss(1,1), t_ts(1,1)) + 30;
	t_end = min(t_gnss(end,1), t_ts(end,1)) - 30;
	t_len = t_end - t_start;
	t_sec = 1 : 1 : t_len;
	% change to relative secs
	t_gnss -= t_start;
	t_ts -= t_start;
	% -----------------------------------------------------
	% get common part of gnss & interpolate each secs
	gnss = [ t_gnss h_gnss];
	% cut common part
	gnss(gnss(:, 1) < 0, :) = [];
	gnss(gnss(:, 1) > t_len, :) = [];
	% change height to relativ in mm
	gnss(:, 2) = (gnss(:, 2) - gnss(1, 2)) * 1000;
	% interpolate to each second
	h_gnss = interp1(gnss(:, 1), gnss(:, 2), t_sec);
	% -----------------------------------------------------
	% get common part of ts & interpolate for missing secs
	ts = [ t_ts h_ts];
	% cut common part
	ts(ts(:, 1) < 0, :) = [];
	ts(ts(:, 1) > t_len, :) = [];
	% change height to relativ in mm
	ts(:, 2) = (ts(:, 2) - ts(1, 2)) * 1000;
	% interpolate to each second
	h_ts = interp1(ts(:, 1), ts(:, 2), t_sec);
	% -----------------------------------------------------
	% cross correlation
	offs = 50;
	xc = xcorr(h_gnss, h_ts, offs);
	di = [-offs:offs];
	[mx mi] = max(xc);
	mdi = di(mi);
	printf('Offset: %d\n', mdi);
	% -----------------------------------------------------
	dh = h_gnss - h_ts;
	figure(1);
	hold off;
	plot(t_sec, h_gnss);
	hold on;
	plot(t_sec, h_ts, "color", 'r');
	plot(t_sec, dh - 60, "color", 'g');
	plot([0 t_len], [-60 -60], "color", 'y');
	title('RTK GNSS & TS');
	xlabel('Time [sec]');
	ylabel('Deflection [mm]');
	% -----------------------------------------------------
	% statistics
	printf('GNSS\n');
	printf('Mean: %.1f mm\n', mean(h_gnss));
	printf('Range: %.1f mm\n', range(h_gnss));
	printf('Std: %.1f mm\n', std(h_gnss));
	printf('TS\n');
	printf('Mean: %.1f mm\n', mean(h_ts));
	printf('Range: %.1f mm\n', range(h_ts));
	printf('Std: %.1f mm\n', std(h_ts));
	printf('Differences\n');
	printf('Mean: %.1f mm\n', mean(dh));
	printf('Range: %.1f mm\n', range(dh));
	printf('Std: %.1f mm\n', std(dh));
