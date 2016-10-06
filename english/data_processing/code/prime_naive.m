% naive solution to find prime numbers
tic();  % start timer
max = 10000; % limit for the max prime number
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:n   % check all dividers
  for j = 2 * i:max % 
    if (mod(j, i) == 0) % modulo of j / i
      p(j) = 0; % mark no prime
    end 
  end
end
prime = find(p); % find nonzeros in p
printf("%d\n", columns(prime));
toc() % write elapsed time
