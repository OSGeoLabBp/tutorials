#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from box import Box

class Rectangle(Box):
    """ class for 2D rectangles """

    def __init__(self, x=0, y=0, p=2, a=1, b=1):

        super(Rectangle, self).__init__(x, y, p, a)
        self.b = b

    def __str__(self):

        return ("{0:." + str(self.p) + "f}, {1:." + str(self.p) + "f}, {2:." +
                str(self.p) + "f}, {3:." + str(self.p) + "f}").format(self.x, self.y, self.a, self.b)

    def area(self):
        """ area of circle """
        return self.a * self.b

    def perimeter(self):
        """ perimeter of circle """
        return 2 * (self.a + self.b)
