Processing GSI file got from Leica DNA03 digital level
======================================================


*Keywords*: Leica GSI, text file reading, conditions, loops, regexp, function

*Data file*: test.gsi

*Program files*: gsi.m, val.m


Sample data

.. code::

    *410001+00000000?......2         Vonal kezdeti és mérési mód 1 = BF 2 = BFFB
    *110002+000000000000000G 83..58+0000000000000000        Kezdőpont és magasság
    *110003+000000000000000G 32...8+0000000001824936 331.08+0000000000159977 390...+0000000000000002 391.08+0000000000000000
    *110004+0000000000000001 32...8+0000000001934475 332.08+0000000000138073 390...+0000000000000002 391.08+0000000000000001
    *110005+0000000000000001 32...8+0000000001934527 336.08+0000000000138071 390...+0000000000000002 391.08+0000000000000002
    *110006+000000000000000G 32...8+0000000001825388 335.08+0000000000159980 390...+0000000000000002 391.08+0000000000000004
    *110007+0000000000000001 571.08-0000000000000005 572.08-0000000000000005 573..8-0000000000109339 574..8+0000000003759663 83..08+0000000000021906
    *110008+0000000000000001 32...8+0000000003143927 331.08+0000000000109401 390...+0000000000000002 391.08+0000000000000005
    *110009+000000000000000F 32...8+0000000003145367 332.08+0000000000178003 390...+0000000000000002 391.08+0000000000000002
    *110010+000000000000000F 32...8+0000000003145992 336.08+0000000000177988 390...+0000000000000002 391.08+0000000000000003
    *110011+0000000000000001 32...8+0000000003145639 335.08+0000000000109382 390...+0000000000000002 391.08+0000000000000002
    *110012+000000000000000F 571.08+0000000000000003 572.08-0000000000000002 573..8-0000000000110236 574..8+0000000010050126 83..08-0000000000046698
    *410013+00000000?......2
    *110014+000000000000000F 83..08-0000000000046698
    *110015+000000000000000F 32...8+0000000003144885 331.08+0000000000177976 390...+0000000000000002 391.08+0000000000000000
    *110016+0000000000000002 32...8+0000000003145350 332.08+0000000000109381 390...+0000000000000002 391.08+0000000000000000*
    ...

Solution in Octave (gsi.m)
--------------------------

.. code:: octave

    % Leica DNA03 GSI file loader
    % input file
    f = fopen('test.gsi', 'r');
    lstart = '';
    while ((line = fgetl(f)) ~= -1)
        line = strtrim(line);
        % remove leading/trailing spaces
        if (line(1) == '*')
            line = substr(line, 2);   % remove * from line start
        endif
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
                endif
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
                endif
                if (length(lstart) == 0)
                    lstart = pid;
                endif
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
                endif
                if (c == '2' || c == '6')
                    % forward reading
                    sumf += val(field);
                endif
            end
        end
    end
    % save last line
    if (length(lstart))
        printf('%4s %4s %1d %9.5f %4.1f\n', lstart, pid, mode, (sumb - sumf) / mode, sumd / mode / 1000.0);
    end
    fclose(f);

*val függvény* (val.m)

.. code:: octave

    function w = val(f)
        dd = [1000, 1000 * 3.28, 0, 0, 0, 0, 10000, 10000 * 3.28, 100000];
        d = dd(str2num(substr(f, 6, 1))+1);
        w = str2num(substr(f, 7)) / d;
    end

*Használat* :

Copy the gsi.m and val.m file into the same folder where the GSI file is.

*Start the program from Octave*:

.. code:: octave

octave:1>cd /path/to/gsi/file
octave:2>gsi

*Start the program from a shell/command window*:

.. code:: bash

octave gsi.m

.. note::

    *Development tipps*  
    Statistical analysis of the staff readings in case of BFFB readings (instrument stability)

