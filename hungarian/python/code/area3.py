"""
    Simple polygon area example version 3
"""
import math
from geom import Point

class Polygon(object):
    """ Polygon class to store border and calculate area
        :param coords: list of Point instants
    """
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)

    def area(self):
        """ Calculates the area of polygon from the coordinates
            :returns: area
        """
        w = 0.0
        for i in range(self.n):
            j = (i + 1) % self.n
            w += (self.coords[j].e + self.coords[i].e) * \
                 (self.coords[j].n - self.coords[i].n)
        return abs(w) /2.0

    def perimeter(self):
        """ Calculates the permeteer of polygon from the coordinates
            :returns: perimeter
        """
        w = 0.0
        for i in range(self.n):
            j = (i + 1) % self.n
            w += math.hypot((self.coords[j].e - self.coords[i].e), \
                 (self.coords[j].n - self.coords[i].n))
        return w

if __name__ == "__main__":
    p0 = Polygon([Point(1, 1), Point(3, 1), Point(2, 2)])
    p1 = Polygon([Point(634110.62 , 232422.09),
        Point(634108.23, 232365.96),
        Point(634066.13, 232378.12),
        Point(634062.95, 232457.58),
        Point(634111.68, 232454.93),
        Point(634110.62, 232422.09)])
    print(p0.area())
    print(p0.perimeter())
    print(p1.area())
    print(p1.perimeter())
