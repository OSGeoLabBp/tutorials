% generate ellipse 
x0 = 1;
y0 = 2;
a = 3;
b = 2;
alfa = pi / 8.0;
%alfa = 0;
n = 40;
t = linspace(0, 2 * pi, n);
dx = a * cos(t);
dy = b * sin(t);
x = x0 + dx * cos(alfa) - dy * sin(alfa); %+ (1 * rand(1, n) - 0.5) / 10;
y = y0 + dy * cos(alfa) + dx * sin(alfa); %+ (1 * rand(1, n) - 0.5) / 10; 
plot(x, y);
f = fopen('ellipse.txt', 'w');
fprintf(f, '%.2f,%.2f\n', [x; y]);
fclose(f);
