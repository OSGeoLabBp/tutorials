#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math
from point import Point

class Circle(Point):
    """ class for 2D circles """

    def __init__(self, x=0, y=0, p=2, r=1):

        super(Circle, self).__init__(x, y, p)
        self.r = r

    def __str__(self):

        return ("{0:." + str(self.p) + "f}, {1:." + str(self.p) + "f}, {2:." +
                str(self.p) + "f}").format(self.x, self.y, self.r)

    def area(self):
        """ area of circle """
        return self.r ** 2 * math.pi

    def perimeter(self):
        """ perimeter of circle """
        return 2 * self.r * math.pi

if __name__ == "__main__":
    # test
    c1 = Circle()
    print(c1)
    print("area: {}".format(c1.area()))
    print("perimeter: {}".format(c1.perimeter()))
    c1 += Point(10,20)
    print(c1)
    c1 = c1 + Point(10,20)
    print(c1)
