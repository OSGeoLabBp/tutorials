#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class Point2D(object):                           # object a bázis osztály
    """ kettő dimenziós pontok osztálya
    """
    def __init__(self, east = 0, north = 0):    # __init__ a konstruktor
        """ Pont inicializálás

            :param east: első koordináta
            :param north: második koordináta
        """ 
        self.east = east            # setter implicit hívása
        self.north = north

    @property
    def east(self):
        """ első koordináta lekérdezése """
        return self._east

    @property
    def north(self):
        """ második koordináta lekérdezése """
        return self._north

    @east.setter
    def east(self, east):
        """ első koordináta beállítása """
        if type(east) in (int, float):
            self._east = east
        else:
            raise Exception("hibás koordináta típus")

    @north.setter
    def north(self, north):
        """ második koordináta beállítása """
        if type(north) in (int, float):
            self._north = north
        else:
            raise Exception("hibás koordináta típus")

    def abs(self):
        """ helyvektor hossza (absolút érték) 
            :returns: absolút érték
        """ 
        return (self._east**2 + self._north**2)**0.5 

    def __abs__(self):
        """ abs függvényhez """
        return self.abs()

    def __str__(self):
        """ Pont szövegláccá alakítása kiiratáshoz

            :returns: a koordináták szövegláncként
        """
        return "{:.3f}; {:.3f}".format(self._east, self._north)

    def __add__(self, p):
        """ Két pont összeadása
            :param p: hozzáadandó pont
            :returns: a két pont összegéből képzett Point2D példányt
        """
        return Point2D(self._east + p.east, self._north + p.north)

if __name__ == "__main__":
    """ tesztelő kód az osztályhoz """
    p0 = Point2D()            # pont az origóban
    p1 = Point2D(5)           # pont 5, 0
    p2 = Point2D(north=6)     # pont 0, 6
    p3 = Point2D(-2, 6)       # pont -2, 6
    try:
        p4 = Point2D([12, 5])
    except:
        print("Hibás inicializálás")
    print(p3)
    print(p3.abs())
    print(abs(p3))            # __abs__ metódus hívása
    print(p3.east)
    p3.east = 99
    print(p3)
