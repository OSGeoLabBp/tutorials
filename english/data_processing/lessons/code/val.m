function w = val(f)
    dd = [1000, 1000 * 3.28, 0, 0, 0, 0, 10000, 10000 * 3.28, 100000];
    d = dd(str2num(substr(f, 6, 1))+1);
    w = str2num(substr(f, 7)) / d;
end
