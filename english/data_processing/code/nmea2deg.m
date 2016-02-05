function deg = nmea2deg(w)
    % convert NMEA dddmm.mmm angle to decimal degree
    p = index(w, '.');
    deg = sscanf(w(1:p-3),'%d') + sscanf(w(p-2:end), '%f') / 60.0;
end
