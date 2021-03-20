#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    compering list processing solutions to generate the list
    multiplied by a constant
"""

import timeit
import numpy as np

def while_loop(m=2.5, n=100_000_000):
    """ using pure while loop """
    i = 0
    l = []
    while i < n:
        l.append(m * i)
        i += 1
    return l

def for_loop(m=2.5, n=100_000_000):
    """ using for loop and range """
    l = []
    for i in range(n):
        l.append(m * i)
    return l

def list_compr(m=2.5, n=100_000_000):
    """ list comprehension """
    return [m * i for i in range(n)]

def map_func(m=2.5, n=100_000_000):
    """ using built in map function """
    return list(map(lambda x: x * 2.5, range(n)))

def numpy_vec(m=2.5, n=100_000_000):
    """ using numpy vector """
    return np.dot(np.arange(n), m)

if __name__ == "__main__":
    print("while loop:        ", timeit.timeit(while_loop, number=1))
    print("for loop:          ", timeit.timeit(for_loop, number=1))
    print("list comprehension:", timeit.timeit(list_compr, number=1))
    print("map function:      ", timeit.timeit(list_compr, number=1))
    print("numpy vector:      ", timeit.timeit(list_compr, number=1))
