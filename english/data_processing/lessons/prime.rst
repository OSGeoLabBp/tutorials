Prime numbers
=============

*Keywords*: algorithm optimalization

*Data file*: none

*Program files:* prime_naive.m, prime_sieve.m, prime_final.m, prime_improved.m, prime_builtin.m, prim1.py, prim2.py, prim3.py, prim3_5.py, prim4.py, prim5.py, prim6.py, prim7.py

Let's write a program to search for prime numbers upto a maximal value. 
We'll make more and more affective solutions.
An integer number is prime if it is only divideable by one and itself.
So the reminder after division should be examined, we need some loops to do it.

Octave solutions
----------------

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

Python solutions
----------------

*First very naive algorithm*

Let's examine the reminder of the division of integer numbers. It is enough to 
examine dividers till the square root of the largest value.

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.0
    """
    import math
    import time

    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, 500001):   # find prims up to 50000
        prime = True
        for divider in range(2, int(math.sqrt(p))+1):
	        if p % divider == 0:     # remainder of division is zero
		        prime = False        # it is not a prime
			if prime:
				prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

*Second naive algorithm*

In the internal loop (for divider) no need to continue with the dividers if a
integer divider found. Exit from the loop with *break* command.

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.1
    """
    import math
    import time

    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, 500001):   # find prims up to 50000
        prime = True
        for divider in range(2, int(math.sqrt(p))+1):
            if p % divider == 0: # remainder of division is zero
                prime = False    # it is not a prime
                break            # divider found no need to continue
        if prime:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

Adding this *break* to the code it runs 5 times faster on my machine.

*Let's make the code more Pythonic*

There is an *else* for *for* loops in Python and this code block is executed 
if we did not jump out the loop before reaching the last value. Let's make the 
code more more flexible, let's read the upper limit for primes from the
command line instead of the hard coded 50000.

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.2
    """
    import math
    import time
    import sys

    max_num = 101
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, max_num):  # find prims up to max_num
        for divider in range(2, int(math.sqrt(p))+1):
            if p % divider == 0: # remainder of division is zero
                break            # divider found no need to continue
        else:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

This change did not make the code more effective but it is more Pythonic and 
more readable.

*A better naive solution*

Each number can be written as the multiplication of prime numbers, so no need
to check the reminder for all values.

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.3
    """
    import math
    import time
    import sys

    max_num = 101
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, max_num):  # find prims up to max_num
        maxp = int(math.sqrt(p))+1
        for divider in prims:    # enough to check prims!
            if p % divider == 0: # remainder of division is zero
                break            # divider found no need to continue
            if maxp < divider:
                prims.append(p)
                break
        else:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

*Effective algorithm*

So far the original idea was improved. There may be a better aproache, idea?
There was a scientist Erastotenes in the achient age who had better idea, the
sieve of Erastotenes. He did not try to divide, but removed the multipliers
of found primes from the list of the possible prime numbers.
Here is the basic solution:

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.0
    """
    import math
    import time
    import sys

    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = list(range(max_num)) # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        numbers[j+j::j] = [0 for k in numbers[j+j::j]] # use sieve
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

List comprehension is used to set multiplyers to zero. It faster and more 
Pythonic then a **for** loop.

.. code:: python

    numbers[j+j::j] = [0 for k in numbers[j+j::j]]

This code is hundred times faster than the firt naive algorithm.

Can it be faster?
-----------------

Let's analyze our code. The *j* loop variable will have the values 2, 3, 4, ...
First we set even numbert from four, then every third numbers from 6, then
every fourth number from 8. Wait, why set we 8, 12, 16 to zero? Those were set 
to zero at the first step. We have to set to zero the multipliers of prims. 
Let's add a condition to the code, clear the list elements only if the *j* th
item was not set ot zero before.

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.1
    """

    import math
    import time
    import sys

    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = range(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = [0 for k in numbers[j+j::j]] # use sieve

    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

Below half million there is no difference in the elapsed time.

Instead of the list comprehension we could use list multiplied integer value
to generate list of zeros, which is faster.

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.2
    """

    import math
    import time
    import sys

    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = range(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = [0] * len(numbers[j+j::j]) # use sieve
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

numpy library can make it faster
--------------------------------

numpy provides a lot of algorithms to solve mathematical problems.
We will use numpy arrays which are more compact than Python lists.
In numpy we can assign one value to a non-continuous range of numpy elements.

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.3
    """

    import math
    import time
    import sys
    import numpy as np

    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = np.arange(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = 0 # use sieve
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

Table of elapsed time of different algorithms for prims upto 100.000, 1.000.000 
and 10.000.000:

+--------+------------------+------------------+------------------+
| Version| Elapsed time [s] | Elapsed time [s] | Elapsed time [s] |
|        |    100000        |   1000000        |  10000000        |
+--------+------------------+------------------+------------------+
|   1.0  |       1.90       |      60          |     N/A          |
+--------+------------------+------------------+------------------+
|   1.1  |       0.45       |      10          |     326          |
+--------+------------------+------------------+------------------+
|   1.2  |       0.44       |      11          |     333          |
+--------+------------------+------------------+------------------+
|   1.3  |       0.21       |       2.62       |      50          |
+--------+------------------+------------------+------------------+
|   2.0  |       0.07       |       0.58       |       6.41       |
+--------+------------------+------------------+------------------+
|   2.1  |       0.04       |       0.32       |       2.99       |
+--------+------------------+------------------+------------------+
|   2.2  |       0.02       |       0.19       |       1.73       |
+--------+------------------+------------------+------------------+
|   2.3  |       0.03       |       0.17       |       1.61       |
+--------+------------------+------------------+------------------+


.. note:: *Development tipps*:

Make a line graph for the time and the maximal number for primes. Include all
algorithms in the graph, to compare them visually.
