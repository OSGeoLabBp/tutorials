Prime numbers
=============

*Keywords*: algorithm optimalization

*Data file*: none

*Program files:* prime_naive.m, prime_sieve.m, prime_final.m, prime_builtin.m

Let's write a program to search for prime numbers upto a maximal value.
An integernumber is prime if it is only divideable by one and itself.
So the reminder after division should be examined, we need some loops to do it.

*Our naive solution* (prime_sieve.m)

.. code:: octave

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

*Result*

.. code:: bash

    octave --no-gui prime_naive.m
    1230
    Elapsed time is 7.51718 seconds.

It is quiet good, 1230 prime number in 8 seconds. Can it be faster?
Let's try to implement sieve of Erasthotenes. Instead of calculating modulo, 
let's clear every second elemet above 2, let's clear every third element 
above 3, etc. This way the if statement canbe removed.

*Sieve of Erasthotenes, first version* (prime_sieve.m)

.. code:: octave

    % first sieve of Erostotenes version
    tic();  % start timer
    max = 1000; % limit for the max prime number
    p = [1:max];  % vector of integer numbers
    n = int64(sqrt(max)); % limit for dividers
    for i = 2:n   % check all dividers
      for j = 2 * i:i:max
        p(j) = 0; % clear 2*i, 3*i, 4*i, ...
      end
    end
    prime = find(p);  % find nonzeros in p
    printf("%d\n", columns(prime));
    toc() % write elapsed time

.. code:: bash

    octave --no-gui -q prime_sieve.m
    1230
    Elapsed time is 0.127878 seconds.

Waw, the elapsed time was reduced nearly 100 times.
Do we need the second nested loop? No we can use array slicing insetad.

*Sieve of Erasthotenes, second version* (prime_final.m)

.. code:: octave

    % second sieve of Erastotenes version
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

.. code:: bash

    octave --no-gui -q prime_final.m
    1230
    Elapsed time is 0.0636721 seconds.

Again reasonable reduction in elapsed time. We used vectoriation to make the
program faster. There is a built in function for prime numbers. Did you know?

*Built in Octave function* (prime_builtin.m)

.. code:: octave

    % built in sieve of Erastothenes version
    tic();  % start timer
    max = 10000;
    prime = primes(max);
    printf("%d\n", columns(prime));
    toc() % write elapsed time

.. code:: bash

    octave --no-gui -q prime_builtin.m
    1229
    Elapsed time is 0.00162506 seconds.

Huge improvement in elapsed time again. Built in functions are the fastest.

.. note:: *Development tipps*:

   Why did we get less primes with the built in function?
