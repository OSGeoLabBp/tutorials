#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math

class Point(object):
    """ class for 2D points """

    def __init__(self, x=0, y=0, p=2):

        self.x = x
        self.y = y
        self.p = 2

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
        """ multiply point ba scalar """
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

if __name__ == "__main__":

    import pandas as pd
    # orientation
    # read coordinates
    df = pd.read_csv('coo.csv')
    pnts = {}                   # new dictionary for points
    # convert data to dictionary of Point objects
    for i in range(df.shape[0]):
        pnts[df['id'][i]] = Point(df['x'][i], df['y'][i])
    # read station target and mean direction from csv file
    df = pd.read_csv('ori.csv')
    # calculate orientation angles
    o = []
    for i in range(df.shape[0]):
        o.append((pnts[df['target'][i]] - pnts[df['station'][i]]).bearing() -
                 df['direction'][i])
    print sum(o) / len(o)
    
    
    
