#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import math
from circle import Circle

class Ellipse(Circle):
    """ class for 2D ellipses """

    def __init__(self, x=0, y=0, p=2, r=1, b=1):

        super(Ellipse, self).__init__(x, y, p, r)
        self.b = b

    def __str__(self):

        return ("{0:." + str(self.p) + "f}, {1:." + str(self.p) + "f}, {2:." +
                str(self.p) + "f}, {3:." + str(self.p) +
                "f}").format(self.x, self.y, self.r, self.b)

    def area(self):
        """ area of ellipse """
        return self.r * self.b * math.pi

    def perimeter(self):
        """ perimeter of ellipse (approximation)"""
        return math.pi * (3 * (self.r + self.b) - ((3 * self.r + self.b) *
            (self.r + 3 * self.b)) ** 0.5)
