% generate ellipse 
a = [ 1; 2; 3; 4];
f = fopen('plane.txt', 'w');
for y = 0:4
  %y += (1 * rand(1, n) - 0.5) / 10; 
  for x = 0:4
    %x += (1 * rand(1, n) - 0.5) / 10;
    z = (a(1) * y + a(2) * x + a(4)) / a(3); % (1 * rand(1, n) - 0.5) / 10;
    fprintf(f, '%.2f,%.2f,%.2f\n', x, y, z);
  end
end
fclose(f);
