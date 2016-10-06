% first sieve of Erasthotenes version
tic();  % start timer
max = 10000; % limit for the max prime number
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:n   % check all dividers
  for j = 2 * i:i:max
    p(j) = 0; % clear 2*i, 3*i, 4*i, ...
  end
end
prime = find(p);  % find nonzeros in p
printf('%d\n', columns(prime));
toc() % write elapsed time
