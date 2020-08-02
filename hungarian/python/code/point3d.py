#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 
from point2d_2 import Point2D 

class Point3D(Point2D): 
    """ háromdimenziós pontok osztálya 

            :param east: első koordináta 
            :param north: második koordináta 
            :param elev: magasság 
    """ 

    def __init__(self, east = 0, north = 0, elev = 0): 
        Point2D.__init__(self, east, north)
        #super(Point3D, self).__init__(east, north) 
        self.elev = elev 

    @property 
    def elev(self): 
        return self._elev 

    @elev.setter 
    def elev(self, elev): 
        if elev < 10000: 
            self._elev = elev 
        else: 
            raise ValueError('elev must be less than 10000') 

    def abs(self): 
        """ helyvektor hossza (absolút érték) 
            :returns: absolút érték
        """
        return (self._east**2 + self._north**2 + self._elev**2)**0.5 

    def __abs__(self): 
        """ abs függvényhez """
        return self.abs() 

    def __str__(self): 
        """ String representation of the 2D point 

            :returns: point coordinates as string (e.g. 5; 3) 
        """ 
        return super(Point3D, self).__str__() + "; {:.3f}".format(self._elev)

if __name__ == "__main__":
    p1 = Point3D(600000,200000,100)
    print(p1)
    print(p1.abs())
    print(abs(p1))
    print(abs(-1))
    print(abs('abc'))
