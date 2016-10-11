Prime numbers
=============

*Keywords*: algorithm optimalization

*Data file*: none

*Program files:* prime_naive.m, prime_sieve.m, prime_final.m, prime_improved.m, prime_improved2.m prime_builtin.m

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
Do we need the second nested loop? No we can use array slicing instead.

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
    for i = 2:max
      p(2*i:i:max) = 0; % clear multipliers of i
    end
    prime = find(p(2:end));  % skip 1 it is not a prime
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_final.m
    1229
    Elapsed time is 0.0636721 seconds.

Again reasonable reduction in elapsed time. We used vectoriation to make the
program faster. Examine again the loop body. If we can save a little time in
the loop body, it may reduce the elapsed time spectacularly.
We clear the same even numers several times, after clearing all even numbers in
the first run of the loop, no need to check any even number again.
Let's move the deletion of even numbers out of the loop and
check only the odd numbers in the loop body.

*Improved sieve of Erastohenes* (prime_improved.m)

.. code:: octave

    % sieve of Erasthotenes third version
    max = 10000; % limit for the max prime number
    if (nargin > 0)
      max = int64(str2num(argv(){1}));
    end
    tic();
    p = [1:max];  % vector of integer numbers
    n = int64(sqrt(max)); % limit for dividers
    p(4:2:max) = 0;  % remove all even numbers
    for i = 3:2:max   % remove multipliers of odd numbers
      p(2*i:i:max) = 0;
    end
    prime = find(p(2:end));  % skip 1 it is not a prime
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_improved.m
    1229
    Elapsed time is 0.051127 seconds.

Should we run the loop till the maximal value? No, if all values are zero
in the rest of the **p** vector we can stop looping. Let's implement it
into our code.

*More impoved sive of Erasthotenes* (prime_improved2.m)

.. code:: octave

    % sieve of Erasthotenes fourth version
    max = 10000; % limit for the max prime number
    if (nargin > 0)
      max = int64(str2num(argv(){1}));
    end
    tic();
    p = [1:max];  % vector of integer numbers
    n = int64(sqrt(max)); % limit for dividers
    p(4:2:max) = 0;  % remove all even numbers
    for i = 3:2:max   % remove multipliers of odd numbers
      if (sum(p(2*i:max)) == 0)
        break;  % no more numbers to test
      end
      p(2*i:i:max) = 0;
    end
    prime = find(p(2:end));  % skip 1 it is not a prime
    toc() % write elapsed time
    printf('%d\n', columns(prime));

.. code:: bash

    octave prime_improved.m
    1229
    Elapsed time is 0.0641479 seconds.

Oops, adding the conditional statement (if)
to the body of loop increased the elapsed time. Let's try the two improved
algorithms for greater primes, prime numbers till 1000000.

.. code:: bash

    octave prime_improved.m 100000
    9592
    Elapsed time is 0.314283 seconds.

    octave prime_improved2.m 100000
    9592
    Elapsed time is 1.78913 seconds.

Unfortunatelly increasing the maximal value the second improvement doesn't
run faster.

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

Huge improvement in elapsed time again. Built in functions are the fastest.

.. note:: *Development tipps*:

Make a line graph for the time and the maximal number for primes. Include all
algorithms in the graph.
