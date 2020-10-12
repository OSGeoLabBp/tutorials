% NMEA parser
f = fopen('nmea1.txt', 'r');
fo = fopen('nmea1.out', 'w');
while (! feof(f))
    buf = fgetl(f);
    bufa = strsplit(buf, ',');
    %checksum bitxor(a,b)
    bufascii = double(buf(2:strcmp(buf, '*')));
    cs = double(buf(2));
    for c = buf(3:end-3)
        cs = bitxor(cs, double(c));
    end
    if (sprintf('%X', cs) ~= buf(end-1:end))
        printf('checksum error\n');
        continue;
    end
    switch (bufa{1})
        case '$GPGGA'
            % GGA, time, latitude, N/S, longitude, E/W, solution type, number of satellitess, hdop, height, M, undulation,M,empty,empty,checksum
            if (str2num(bufa{7}) == 1)
                % use only GPS fix
                lat = nmea2deg(bufa{3});
                if (bufa{4} == 'S')
                    lat = -lat;
                end
                lon = nmea2deg(bufa{5});
                if (bufa{6} == 'W')
                    lon = 360.0 - lon;
                end
                height = str2num(bufa{10});
                fprintf(fo, '%.6f,%.6f,%.2f\n', lat, lon, height);
            end
    end
end
fclose(f);
fclose(fo);