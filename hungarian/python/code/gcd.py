def gcd_naiv(a, b):
    """ find greatest common divisor of a and b """
    for i in range(min(a, b), 1, -1):
        if a % i == 0 and b % i == 0:
            return i
    return 1

def gcd_rec(a, b):
    """ find greatest common divisor of a and b, recursive Euclid's algorithm"""
    if b == 0:
        return a
    return gcd_rec(b, a % b)

def gcd(a, b)
    """ find greatest common divisor of a and b, non-recursive Euclid's algorith"""
    while b:
        a, b = b, a % b
    return a
