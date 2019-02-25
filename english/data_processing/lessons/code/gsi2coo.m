% Leica GSI coordinate loader
% input file
f = fopen('labor.gsi', 'r');
% output file
fo = fopen('labor.csv', 'w');
while ((line = fgetl(f)) ~= -1)  % read input line by line
    x = y = elev = 0;  % default coordinates
    line = strtrim(line);  % remove leading/trailing spaces
    if (line(1) == '*')  % remove * from line start
        line = substr(line, 2);
    end
    fields = strsplit(line, ' ');
    [ncol, nrow] = size(fields);  % number of columns and rows in cell array
    for i = 1:nrow
        field = fields{i};  % element from cell array
        switch (substr(field, 1, 2))
        case '11'  % point number, leading zeros removed
            pid = regexprep(substr(field, 8), '^0+', '');
            if (length(pid) == 0)
            pid = '0';
            end
        case '81'  % easting
            x = val(field);
        case '82'  % northing
            y = val(field);
        case '83'  % elevation
            elev = val(field);
        end
    end
    % write coordinates to stadard output
    fprintf(fo, '%s,%.3f,%.3f,%.3f\n', pid, x, y, elev);
end
fclose(f);
fclose(fo);
