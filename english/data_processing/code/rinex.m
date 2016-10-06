fin = fopen ('brdc1520.15n', 'r');
% skip header lines
text_line = fgetl (fin);
while (! feof (fin) )
  if strfind(text_line, 'END OF HEADER')
    break;
  end
  text_line = fgetl(fin);
end
text_line = fgetl(fin);
while (! feof (fin) )
    [sat_id, year, month, day, hour, min, sec] = ...
      sscanf(substr(text_line, 1, 22), '%2i %2i %2i %2i %2i %2i %4f', 'C')
    s = zeros(29,1);
    % replace D with E
    w = strrep(substr(text_line, 23), 'D', 'E');
    s(1:3) = sscanf(w, '%19g%19g%19g');
    text_line = fgetl(fin);
    i = 4;
    for j = 1:6
      w = strrep(text_line, 'D', 'E');
      s(i:i+3) = sscanf(w, '     %19g%19g%19g%19g');
      text_line = fgetl(fin);
      i += 4;
    end
    w = strrep(text_line, 'D', 'E');
    s(28:29) = sscanf(w, '     %19g%19g');
    text_line = fgetl(fin);
    % add here your code to filter data ...
    s
end
fclose (fin);
