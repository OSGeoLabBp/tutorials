% regression 
version = '1.0 alpha';
global eps = 1e-4;      % limit for parameter change in iteration
global max_iter = 1000;  % maximal number of iteration

pkg load statistics

% function to mimic ternary operator
% param expr - boolean expression
%       true_val - returned value if expr true
%       false_val- returned value if expr false   
function retval = ternary (expr, true_val, false_val)
  if (expr)
    retval = true_val;
  else
    retval = false_val;
  end
end

% regression circle
% param  points - input coordinates (n x 2)
% output x0, y0 - center of circle
%        r - radius
function [x0, y0, r] = circle(points)
  res=[points(:,1) points(:,2) ones(rows(points),1)] \ [-(points(:,1).^2+points(:,2).^2)];
  x0 = -0.5 * res(1);
  y0 = -0.5 * res(2);
  r = sqrt((res(1)^2 + res(2)^2) / 4 - res(3));
end

% fit horizontal ellipse (no rotation)
% param  points - input coordinates (n x 2)
% output x0, y0 - center of ellipse
%        a, b   - length of semi axis
%        m      - iteration number
function [x0, y0, a, b, m] = ellipse(points)
  global eps
  global max_iter
  
  [x0, y0, a] = circle(points);   % approximate value from circle
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

% fit rotated ellipse
% param  points - input coordinates (n x 2)
% output x0, y0 - center of ellipse
%        a, b   - length of semi axis
%        aplha  - rotational angle
%        m      - iteration number
function [x0, y0, a, b, alpha, m] = rot_ellipse(points)
  % eigen vectors & rotated, shifted points
  [e, p] = princomp(points);
  % shift of points
  x0 = mean(points(:, 1)) - mean(p(:, 1));
  y0 = mean(points(:, 2)) - mean(p(:, 2));
  % rotational angle
  alpha = atan2(e(2, 1), e(1, 1));
  alpha = ternary(alpha < 0, alpha + 2 * pi, alpha);
  alpha = ternary(alpha > pi, alpha - pi, alpha);
  [wx0, wy0, a, b, m] = ellipse(p);
end

% get random points
% param  points - input coordinates (n x 2)
%        k      - number of random points to return
% output x0, y0 - center of ellipse
%        a, b   - length of semi axis
%        aplha  - rotational angle
function pp = randp(points, k)
  w = points;
  n = rows(points);
  for i = 1:n
    j = 1 + floor(rand() * n);
    w1 = points(i, :);
    w(i, :) = w(j, :);
    w(j, :) = w1;
  end
  pp = w(1:k, :);
end

% monte carlo robust estimation of ellipse parameters
% param  points - input coordinates (n x 2)
%        k      - number of random points to use
% output x0, y0 - center of ellipse
%        a, b   - length of semi axis
%        aplha  - rotational angle
function [x0, y0, a, b, alpha] = mc_ellipse(points, k)
  pars = zeros(k, 5);
  for i = 1:k
    p = randp(points, k);
    [x0, y0, a, b, alpha, m] = rot_ellipse(p);
    pars(i, :) = [x0, y0, a, b, alpha];
  end
  x0 = sort(pars(:, 1))(floor(k / 2));
  y0 = sort(pars(:, 2))(floor(k / 2));
  a = sort(pars(:, 3))(floor(k / 2));
  b = sort(pars(:, 4))(floor(k / 2));
  alpha = sort(pars(:, 5))(floor(k / 2));
  pars
end

% horizontal ellipse
points0 = dlmread('horiz_ellipse.txt');
[x0, y0, a, b, m] = ellipse(points0); 
printf('x0=%.2f y0=%.2f a=%.2f b=%.2f m=%d\n', x0, y0, a, b, m);
% rotated ellipse
points1 = dlmread('rot_ellipse.txt');
[x0, y0, a, b, alpha, m] = rot_ellipse(points1);
printf('x0=%.2f y0=%.2f a=%.2f b=%.2f alpha=%.4f m=%d\n', ...
  x0, y0, a, b, alpha * 180.0 / pi, m);
% robust monte carlo
[x0, y0, a, b, alpha] = mc_ellipse(points1, 10);
printf('x0=%.2f y0=%.2f a=%.2f b=%.2f alpha=%.4f\n', ...
  x0, y0, a, b, alpha * 180.0 / pi);
