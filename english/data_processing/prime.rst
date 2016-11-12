Prime numbers
=============

*Keywords*: algorithm optimalization

*Data file*: none

*Program files:* prime_naive.m, prime_sieve.m, prime_final.m, prime_improved.m, prime_builtin.m

Let's write a program to search for prime numbers upto a maximal value. 
We'll make more and more affective solutions.
An integer number is prime if it is only divideable by one and itself.
So the reminder after division should be examined, we need some loops to do it.

*Our naive solution* (prime_naive.m)

.. code:: octave

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

*Result*

.. code:: bash

    octave prime_naive.m
    1229
    Elapsed time is 7.51718 seconds.

It is quiet good, 122 prime numbers in 8 seconds. Can it be faster?
Let's try to implement sieve of Erasthotenes. Instead of calculating modulo, 
let's clear every second elemet above 2, let's clear every third element 
above 3, etc. This way the if statement can be removed.

.. note::

   Timing is not exact. If you run the program twice you'll get slitely
   different elapsed times.

*Sieve of Erasthotenes, first version* (prime_sieve.m)

.. code:: octave

    % sieve of Erasthotenes first version
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

.. code:: bash

    octave prime_sieve.m
    1229
    Elapsed time is 0.127878 seconds.

Waw, the elapsed time was reduced nearly 100 times. Let's try to make it
faster.
Do we need the second nested loop? No, we can use array slicing instead.
Do we need to remove multiplier of 4 after removing all multipliers of 2?
No, we have to remove multipliers of numbers which are in the sieve (where p(i)
is not zero).

*Sieve of Erasthotenes, second version* (prime_final.m)

.. code:: octave

    % sieve of Erasthotenes second version
    max = 10000; % limit for the max prime number
    if (nargin > 0)
      max = int64(str2num(argv(){1}));
    end
    tic();
    p = [1:max];  % vector of integer numbers
    n = int64(sqrt(max)); % limit for dividers
    for i = 2:n
      if p(i) > 0
        p(2*i:i:max) = 0; % clear multipliers of i
      end
    end
    prime = find(p(2:end));  % skip 1 and clear zeros
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_final.m
    1229
    Elapsed time is 0.000763893 seconds.

Again huge reduction in elapsed time. We used vectoriation to make the
program faster and we reduced the number of excution of the loop body. 
Examine again the loop body. If we can save a little time in the loop body, 
it may reduce the elapsed time spectacularly.

Should we run the loop till the maximal value (n)? No, if all values are zero
in the rest of the **p** vector we can stop looping. Let's implement it
into our code.

*More impoved sive of Erasthotenes* (prime_improved.m)

.. code:: octave

    % sieve of Erasthotenes fourth version
    max = 10000; % limit for the max prime number
    if (nargin > 0)
      max = int64(str2num(argv(){1}));
    end
    tic();
    p = [1:max];  % vector of integer numbers
    n = int64(sqrt(max)); % limit for dividers
    for i = 2:n   % remove multipliers of odd numbers
      if p(i) > 0
        p(2*i:i:max) = 0;
      elseif (sum(p(i:max)) == 0)
        break;  % no more numbers to test
      end
    end
    prime = find(p(2:end));  % skip 1 it is not a prime
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_improved.m
    1229
    Elapsed time is 0.00265098 seconds.

Oops, adding the else part to the conditional statement (elseif)
to the body of loop increased the elapsed time. It may save time for larger
limit, try to test it.

There is a built in function for prime numbers in Octave. Did you know?

*Built in Octave function* (prime_builtin.m)

.. code:: octave

    % built in sieve of Erasthotenes version
    max = 10000; % limit for the max prime number
    if (nargin > 0)
      max = int64(str2num(argv(){1}));
    end
    tic();  % start timer
    prime = primes(max);
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_builtin.m
    1229
    Elapsed time is 0.00162506 seconds.

Elapsed time not reduced compering to prime_final.m.
Try to increase the maximal prime value from the command line, the elapsed time
for built in prime function increases slower and becomes faster.
Built in functions are usually the fastest.

.. note:: *Development tipps*:

Make a line graph for the time and the maximal number for primes. Include all
algorithms in the graph, tocompare then visually.
