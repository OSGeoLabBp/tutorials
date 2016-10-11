% naive solution to find prime numbers
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1})); % get command line argument for max
end
tic();  % start timer
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:n   % check all dividers
  for j = 2 * i:max % 
    if (mod(j, i) == 0) % modulo of j / i
      p(j) = 0; % mark no prime
    end 
  end
end
prime = find(p(2:end));  % skip 1 it is not a prime
toc() % write elapsed time
printf('%d\n', columns(prime));
