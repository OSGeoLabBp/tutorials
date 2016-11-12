% sieve of Erasthotenes third version
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1}));
end
tic();
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
for i = 2:n  % remove multipliers of odd numbers
  if p(i) > 0    % not cleared yet
    p(2*i:i:max) = 0;
  elseif (sum(p(i:max)) == 0)
      break;       % no more numbers to test
  end
end
prime = find(p(2:end));  % skip 1 and clear zeros
toc() % write elapsed time
printf('%d\n', columns(prime));
