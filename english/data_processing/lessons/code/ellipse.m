% regression 
version = '1.0 alpha';
global eps = 1e-4;      % limit for parameter change in iteration
global max_iter = 1000;  % maximal number of iteration

% regression circle
function [x0, y0, r] = circle(points)
  res=[points(:,1) points(:,2) ones(rows(points),1)] \ [-(points(:,1).^2+points(:,2).^2)];
  x0 = -0.5 * res(1);
  y0 = -0.5 * res(2);
  r = sqrt((res(1)^2 + res(2)^2) / 4 - res(3));
end

% fit ellipse no rotation
function [x0, y0, a, b, m] = ellipse(points)
  global eps
  global max_iter
  
  % approximate value from circle
  [x0, y0, a] = circle(points);
  b = a;
  n = rows(points);
  m = 0;    % actual iteration number
  while (true)
    % parameters
    t = atan2((points(:,2) - y0) / b , (points(:,1) - x0) / a);
    res1 = [ones(n, 1) cos(t)] \ (points(:, 1) - a * cos(t) - x0);
    x0 += res1(1);
    a += res1(2);
    res2 = [ones(n, 1) sin(t)] \ (points(:, 2) - b * sin(t) -y0);
    y0 += res2(1);
    b += res2(2);
    if (abs(res1(1)) <= eps && abs(res1(2)) <= eps && ...
        abs(res2(1)) <= eps && abs(res2(2)) <= eps)
      break
    end
    m++;
    if (m > max_iter)
      printf('maxiter\n');
      a = b = -1;
      break
    end
  end
end

% read points
points = dlmread('horiz_ellipse.txt');
[x0, y0, a, b, m] = ellipse(points); 
printf('x0=%.2f y0=%.2f a=%.2f b=%.2f m=%d\n', x0, y0, a, b, m);
