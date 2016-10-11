% built in sieve of Erasthotenes version
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1}));
end
tic();  % start timer
prime = primes(max);
toc() % write elapsed time
printf('%d\n', columns(prime));
