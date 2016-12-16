"""
    Simple polygon area example version 2
"""

class Polygon(object):
    """ Polygon class to store border and calculate area
        :param coords: list of lists of coordinate pairs [[1, 2], [3, 5], [2, 6]]
    """
    def __init__(self, coords):
        self.coords = coords

    def area(self):
        """ Calculate the area of polygon from the coordinates
            :returns: area
        """
        w = 0.0
        for i in range(len(self.coords)):
            j = (i + 1) % len(self.coords)
            w += (self.coords[j][0] + self.coords[i][0]) * \
                 (self.coords[j][1] - self.coords[i][1])
        return abs(w) /2.0

if __name__ = "__main__":
    p0 = Polygon([[1, 1], [3, 1], [2, 2]])
    p1 = Polygon([[634110.62 , 232422.09 ],
        [634108.23, 232365.96],
        [634066.13, 232378.12],
        [634062.95, 232457.58],
        [634111.68, 232454.93],
        [634110.62, 232422.09]])
    print(p0.area())
    print(p1.area())
