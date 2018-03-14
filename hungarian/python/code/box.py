#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from point import Point

class Box(Point):
    """ class for 2D boxes """

    def __init__(self, x=0, y=0, p=2, a=1):

        super(Box, self).__init__(x, y, p)
        self.a = a

    def __str__(self):

        return ("{0:." + str(self.p) + "f}, {1:." + str(self.p) + "f}, {2:." +
                str(self.p) + "f}").format(self.x, self.y, self.a)

    def area(self):
        """ area of circle """
        return self.a ** 2

    def perimeter(self):
        """ perimeter of circle """
        return 4 * self.a
