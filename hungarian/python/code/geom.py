import math
from angle import Angle

class Point(object):
    """ class to handle 2D points
        :param e: easting of point (float)
        :param n: northing of point (float)
    """

    def __init__(self, e=0, n=0):
        self.e = e
        self.n = n

    def __str__(self):
        """ print helper method
        """
        return "Point(%.2f, %.2f)" % (self.e, self.n)

    def __add__(self, p):
        """ add the coordinates of two points
            :param p: point to add
            :returns: a new point or child class
        """
        return self.__class__(self.e + p.e, self.n + p.n)   # create instance of self

    def __iadd__(self, p):
        """ increment coordinates by an other point
            :param p: point to add
            :returns: the incremented instance
        """
        self.e += p.e
        self.n += p.n
        return self

    def __sub__(self, p):
        """ substract coordinates of another point
            :param p: point to add (Point)
            :returns: a new point or child class instance
        """
        return self.__class__(self.e - p.e, self.n - p.n)

    def dist(self):
        """ distance from origin
            :returns: distance from origin (float)
        """
        return math.hypot(self.e, self.n)

    def wcb(self):
        """ whole circle bearing from the origin
            :returns: whole circle bearing (Angle)
        """
        return Angle(math.atan2(self.e, self.n))

    def polar(self, a, d):
        """ Polar point calculation
            :param a: polar angle from north clockwise (Angle)
            :param d: polar distance (float)
            :returns: a new point
        """
        return self.__class__(self.e + math.sin(a.val) * d,
                              self.n + math.cos(a.val) * d)

class Circle(Point):
    """ class to handle circles
        :param e: easting of point (float)
        :param n: northing of point (float)
        :param r: radius (float)
    """

    def __init__(self, e=0, n=0, r=1):
        self.r = r
        super(Circle, self).__init__(e, n)  # call parent's constructor

    def __str__(self):
        """ print helper method
        """
        return "Circle(%.2f, %.2f R=%.2f)" % (self.e, self.n, self.r)

    def area(self):
        """ area of circle
            :returns: area of circle
        """
        return math.pi * self.r ** 2.0

    def perimeter(self):
        """ perimeter of circle
            :returns: perimeter of circle
        """
        return math.pi * self.r * 2.0

    def center(self):
        """ get center as a Point object
            :returns: center of circle (Point)
        """
        return Point(self.e, self.n)

    def __mul__(self, c):
        """ intersections of circles using '*' operator
            :param c: another circle (Circle)
            :returns: tuple of intersection points (Point)
        """
        p0 = self.center()
        d = (p0 - c.center()).dist()
        if d > self.r + c.r:
            # no intersection empty tuple
            return ()
        a = (self.r ** 2 - c.r ** 2 + d ** 2) / 2.0 / d
        h = math.sqrt(self.r ** 2 - a ** 2)
        de = c.e - self.e
        dn = c.n - self.n
        p2 = p0 + Point(a * de / d, a * dn / d)
        w1 = h * dn / d
        w2 = h * de / d
        pp1 = p2 + Point(w1, -w2)
        pp2 = p2 + Point(-w1, w2)
        return (pp1, pp2)

class Line(Point):
    """ class to handle infinite lines
        :param e: easting of point (float)
        :param n: northing of point (float)
        :param angle: angle from north clockwise (Angle)
    """
    
    def __init__(self, e=0, n=0, angle=0):
        if isinstance(angle, Angle):
            self.angle = angle
        else:
            self.angle = Angle(angle)
        super(Line, self).__init__(e, n)  # call parent's constructor

    def rotate(self, a):
        """ rotate
            :param a: rotation angle clockwise (Angle)
        """
        self.angle += a

    def equation(self):
        """ calculate line equation coefficients a * e + b * n + c = 0
            :returns: tuple of a, b, c
        """
        a = math.cos(self.angle.val)
        b = -math.sin(self.angle.val)
        c = - a * self.e - b * self.n
        return (a, b, c)

    def __mul__(self, l):
        """ intersection of two lines using '*' operator
            :param l: line to intersect with (Line)
            :returns: intersection point (Point)
        """
        l1 = self.equation()
        l2 = l.equation()
        w = l1[0] * l2[1] - l1[1] * l2[0]
        if abs(w) > 1e-5:                # check for paralel lines
            e = (l1[1] * l2[2] - l1[2] * l2[1]) / w
            n = (l1[2] * l2[0] - l1[0] * l2[2]) / w
            return Point(e, n)
        return None

    def __str__(self):
        """ print helper method
        """
        return "Line(%.2f, %.2f %s)" % (self.e, self.n, self.angle)
    
class Text(Line):
    """ class to handle text
        :param e: easting of point (float)
        :param n: northing of point (float)
        :param angle: angle from north clockwise (Angle)
        :param txt: text (string)
    """

    def __init__(self, e=0, n=0, angle=0, txt='hello'):
        self.txt = txt
        super(Text, self).__init__(e, n, angle)  # call parent's constructor

    def __str__(self):
        """ print helper method
        """
        return "Text(%.2f, %.2f %s %s)" % (self.e, self.n, self.angle, self.txt)

class Rectangle(Line):
    """ class to handle rotated rectangle
        :param e: easting of point (float)
        :param n: northing of point (float)
        :param angle: angle from north clockwise (Angle)
        :param width: width of rectangel (float)
        :param height: height of rectngle (float)
    """
    def __init__(self, e=0, n=0, angle=0, width=1, height=1):
        self.width = width
        self.height = height
        super(Rectangel, self).__init__(e, n, angle)  # call parent's constructor

    def area(self):
        """ area of rectangle
            :returns: area (float)
        """
        return self.width * self.height

    def perimeter(self):
        """ perimeter of rectangle
            :returns: perimeter
        """
        return (self.width + self.height) * 2.0
    
    def __str__(self):
        """ print helper method
        """
        return "Rectangle(%.2f, %.2f %s %s)" % (self.e, self.n, self.angle, self.txt)

if __name__ == "__main__":
    # tests for point class
    p1 = Point(5, 8)
    print(p1)
    p2 = p1 + Point(1, 2)
    print(p2)
    a2 = (p2-p1).wcb().normalize()      # bearing from p1 to p2
    print(a2)
    print((p2-p1).dist())               # distance between p1 and p2
    p3 = p1 + Point(1, -2)
    print(p3)
    a3 = (p3-p1).wcb().normalize()      # bearing from p1 to p3
    print(a3)
    p4 = p1 - Point(1, 2)
    print(p4)
    a4 = (p4-p1).wcb().normalize()      # bearing from p1 to p4
    print(a4)
    p5 = p1 + Point(-1, 2)
    print(p5)
    a5 = (p5-p1).wcb().normalize()      # bearing from p1 to p5
    print(a5)
    print(p1.polar(Angle('12-34-56'), 2.456))   # a polar point
    # tests for line
    print("-------------------")
    l1 = Line(p2.e, p2.n, (p1-p2).wcb().normalize())
    l2 = Line(p3.e, p3.n, (p1-p3).wcb().normalize())
    l3 = Line(p4.e, p4.n, (p1-p4).wcb().normalize())
    l4 = Line(p5.e, p5.n, (p1-p5).wcb().normalize())
    print(l1 * l2)                       # intersection of lines
    print(l1 * l4)                       # intersection of lines
    print(l2 * l3)                       # intersection of lines
    print(l3 * l4)                       # intersection of lines
    # test for circle
    print("-------------------")
    c1 = Circle(6, 8, 4)
    print(c1)
    print(c1.area())
    print(c1.perimeter())
    c2 = Circle(8, 5, 5)
    print(c2)
    for p in (c1 * c2):
        print(p)
