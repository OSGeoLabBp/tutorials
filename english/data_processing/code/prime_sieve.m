% first sieve of Erasthotenes version
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1}));
end
tic();  % start timer
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:n   % check all dividers
  for j = 2 * i:i:max
    p(j) = 0; % clear 2*i, 3*i, 4*i, ...
  end
end
prime = find(p(2:end));  % skip 1 it is not a prime
toc() % write elapsed time
printf('%d\n', columns(prime));
