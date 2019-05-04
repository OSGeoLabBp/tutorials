#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

class Point(object):
    """ class for 2D points
        x, y - position of point, default 0,0
        p - decimals in coordinate output, default 2
    """
    def __init__(self, x=0, y=0, p=2):

        self.x = x
        self.y = y
        self.p = p

    def __str__(self):
        """ for print """
        return ("{0:." + str(self.p) + "f}, {1:." + str(self.p) +
                "f}").format(self.x, self.y)

    def bearing(self):
        """ angle of vector to point """
        return math.atan2(self.y, self.x)

    def __abs__(self):
        """ the length of the vector to the point """
        return math.hypot(self.x, self.y)

    def __sub__(self, b):
        """ difference of two points """
        return Point(self.x - b.x, self.y - b.y)

    def __isub__(self, b):
        """ decrement point """
        self.x -= b.x
        self.y -= b.y
        return self

    def __add__(self, b):
        """ add two points """
        return Point(self.x + b.x, self.y + b.y)
    
    def __iadd__(self, b):
        """ increment point """
        self.x += b.x
        self.y += b.y
        return self

    def __mul__(self, c):
        """ multiply point by scalar """
        return Point(self.x * c, self.y * c)

    def __imul__(self, c):
        """ """
        self.x *= c
        self.y *= c
        return self

    def move(self, x_offset, y_offset):
        """ move point """
        return self.__iadd__(Point(x_offset, y_offset))

    def polar(self):
        """ return distance and direction """
        return self.__abs__(), self.bearing()

    def rect(self, dist, ang):
        """ convert polar to rectangular """
        self.x = dist * math.cos(ang)
        self.y = dist * math.sin(ang)

def PolarP(dist, ang):
    """ polar to rectangular coordinates returning Point """
    return Point(dist * math.cos(ang), dist * math.sin(ang))

if __name__ == "__main__":
    # tests
    v = 0.1
    A = Point(-100.4627, 52.5957)
    B = Point(11.0532, 52.5956)
    dist, bea = (B - A).polar()
    P1 = A + PolarP(v, bea + math.pi * 3 / 2) 
    P2 = P1 + PolarP(dist, bea)
    P3 = P2 + PolarP(v, bea + math.pi / 2)
    P4 = A + PolarP(v, bea +math.pi / 2)
    print(P1)
    print(P2)
    print(P3)
    print(P4)
