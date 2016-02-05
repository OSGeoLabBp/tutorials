% Leica DNA03 GSI file loader
% input file
f = fopen('test.gsi', 'r');
lstart = '';
while ((line = fgetl(f)) ~= -1)
    line = strtrim(line);
    % remove leading/trailing spaces
    if (line(1) == '*')
        line = substr(line, 2);   % remove * from line start
    end
    fields = strsplit(line, ' ');
    [ncol, nrow] = size(fields);
    % number of columns and rows in cell array
    for i = 1:nrow
        field = fields{i};    % element from cell array
        switch (substr(field, 1, 2))
        case '41'
            % store previous leveling line
            if (length(lstart))
                printf('%4s %4s %1d %9.5f %4.1f\n', lstart, pid, mode, (sumb - sumf) / mode, sumd / mode / 1000.0);
            end
            % new levelling line initialization
            lstart = '';
            sumb = 0;
            sumf = 0;
            sumd = 0;
            mode = str2num(field(length(field)));     % 1-BF, 2-BFFB
        case '11'
            % point number, leading zeros removed
            pid = regexprep(substr(field, 8), '^0+', '');
            if (length(pid) == 0)
                pid = '0';
            end
            if (length(lstart) == 0)
                lstart = pid;
            end
        case '83'
            % elevation
            elev = val(field);
        case '32'
            % distance
            sumd += val(field);
        case '33'
            % staff reading
            c = field(3);
            if (c == '1' || c == '5')
                % back reading
                sumb += val(field);
            end
            if (c == '2' || c == '6')
                % forward reading
                sumf += val(field);
            end
        end
    end
end
% save last line
if (length(lstart))
    printf('%4s %4s %1d %9.5f %4.1f\n', lstart, pid, mode, (sumb - sumf) / mode, sumd / mode / 1000.0);
end
fclose(f);
