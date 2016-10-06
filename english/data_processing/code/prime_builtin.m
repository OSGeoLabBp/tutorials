% built in sieve of Erasthotenes version
max = 10000;
tic();  % start timer
prime = primes(max);
printf('%d\n', columns(prime));
toc() % write elapsed time
