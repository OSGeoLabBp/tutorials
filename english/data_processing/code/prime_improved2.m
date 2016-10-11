% sieve of Erasthotenes fourth version
max = 10000; % limit for the max prime number
if (nargin > 0)
  max = int64(str2num(argv(){1}));
end
tic();
max = 10000; % limit for the max prime number
p = [1:max];  % vector of integer numbers
n = int64(sqrt(max)); % limit for dividers
p(4:2:max) = 0;  % remove all even numbers
for i = 3:2:max   % remove multipliers of odd numbers
  if (columns(find(p(2*i:max))) == 0)
    disp(2*i);
    break;  % no more numbers to test
  end
  p(2*i:i:max) = 0;
end
prime = find(p(2:end));  % skip 1 it is not a prime
toc() % write elapsed time
printf('%d\n', columns(prime));
