"""
    Sieve of Erasthotenes prim algorithm
    version 2.2
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
