"""
    Simple polygon area example version 3
"""
import math
import sys
from geom import Point

class Polygon(object):
    """ Polygon class to store border and calculate area
        :param coords: list of Point instants
    """
    def __init__(self, coords=[]):
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

def Txt2PntList(txt):
    """ Convert a string to list of points
        e.g. "1 2 4 6 -1 2" -> [Point(1,2), Point(4, 6), Point(-1, 2)]
    """
    # change string to list of floats
    fl = [float(item) for item in txt.strip().split()]
    # generate easting, northing list
    return [Point(*i) for i in zip(fl[::2], fl[1::2])]
 
if __name__ == "__main__":
    # read polygons from file and calculate areas
    fn = "polys.txt"
    if len(sys.argv) > 1:
        fn = sys.argv[1]
    i = 0
    with open(fn, "r") as lines:
        for line in lines:
            i += 1
            print("{:4d} {:12.2f}".format(i, Polygon(Txt2PntList(line)).area()))
