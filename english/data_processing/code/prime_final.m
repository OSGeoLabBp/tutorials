% sieve of Erasthotenes second version
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1}));
end
tic();
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:max
  p(2*i:i:max) = 0; % clear multipliers of i
end
prime = find(p(2:end));  % skip 1 it is not a prime
toc() % write elapsed time
printf('%d\n', columns(prime));
