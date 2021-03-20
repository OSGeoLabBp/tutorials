#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    compering the effectiveness of different loop constructions in Python
    base on https://www.youtube.com/watch?v=Qgevy75co8c

    the sum of the first n integer values will be summed up using
    different approaches
"""
import timeit
import numpy as np

def while_loop(n=100_000_000):
    """ using pure while loop """
    i = 0
    s = 0
    while i < n:
        s += i
        i += 1
    return s

def for_loop(n=100_000_000):
    """ using for and range """
    s = 0
    for i in range(n):
        s += i
    return s

def sum_func(n=100_000_000):
    """ using built in sum function """
    return sum(range(n))

def numpy_sum(n=100_000_000):
    """ using numpy arange and sum """
    return np.sum(np.arange(n))

def math_logic(n=100_000_000):
    """ using math formula """
    return n * (n + 1) // 2

if __name__ == "__main__":
    print("while loop:   ", timeit.timeit(while_loop, number=1))
    print("for loop:     ", timeit.timeit(for_loop, number=1))
    print("sum function :", timeit.timeit(sum_func, number=1))
    print("numpy sum    :", timeit.timeit(numpy_sum, number=1))
    print("math logic   :", timeit.timeit(math_logic, number=1))
