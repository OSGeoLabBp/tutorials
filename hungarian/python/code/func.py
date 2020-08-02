#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 
from math import (sqrt, prod) 

def celsius(fahrenheit=0): 
    "celsius to fahrenheit conversion"
    return (fahrenheit - 32) * 5.0 / 9.0 

def root(a, b, c): 
    "roots of a quadratic equation" 
    d = b**2 - 4 * a * c 
    if d == 0: 
        return -b / 2.0 / a 
    elif d > 0: 
        return ((-b + sqrt(d)) / 2.0 / a, (-b - sqrt(d)) / 2.0 / a) 
    else: 
        pass	# complex roots solved later
    return None 

def f(n): 
    "factorial calculation with while" 
    f = 1 
    while n > 0: 
        f *= n 
        n -= 1 
    return f 

def fact(n): 
    "factorial calculation with for" 
    f = 1 
    for i in range(1, n+1): 
        f *= i 
    return f 

def factor(n): 
    "recursive faktorial calculation" 
    if n <= 1: 
        return 1 
    return n * factorial(n-1) 

def factorial(n):
	""" PYthonikus megoldás 3.8+ """
	return prod(range(1, n+1))

if __name__ == "__main__":

	from timeit import timeit
	print(timeit('f(100)', 'from func import f', number=1000000))
	print(timeit('fact(100)', 'from func import fact', number=1000000))
	print(timeit('factor(100)', 'from func import factor', number=1000000))
	print(timeit('factorial(100)', 'from func import factorial', number=1000000))
