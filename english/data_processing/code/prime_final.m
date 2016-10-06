% first sieve of Erasthotenes version
tic();
max = 10000; % limit for the max prime number
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:max
  p(2*i:i:max) = 0; % clear multipliers of i
end
prime = find(p);
printf("%d\n", columns(prime));
toc()
