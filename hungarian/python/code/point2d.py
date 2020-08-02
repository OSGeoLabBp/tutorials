#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

class Point2D(object):                           # object a bázis osztály
    """ kétdimenziós pontok osztálya
    """
    def __init__(self, east = 0, north = 0):    # __init__ a konstruktor
        """ Pont inicializálás

            :param east: első koordináta
            :param north: második koordináta
        """ 
        self.setEast(east)
        self.setNorth(north)

    def setEast(self, east):
        """ első koordináta beállítása """
        if type(east) in (int, float):
            self.__east = east
        else:
            raise Exception("hibás koordináta típus")

    def setNorth(self, north):
        """ második koordináta beállítása """
        if type(north) in (int, float):
            self.__north = north
        else:
            raise Exception("hibás koordináta típus")

    def getEast(self):
        """ első koordináta lekérdezése """
        return self.__east

    def getNorth(self):
        """ második koordináta lekérdezése """
        return self.__north

    def abs(self):
        """ helyvektor hossza (absolút érték) 
            :returns: absolút érték
        """ 
        return (self.__east**2 + self.__north**2)**0.5 

    def __str__(self):
        """ Pont szövegláccá alakítása kiiratáshoz

            :returns: a koordináták szövegláncként
        """
        return "{:.3f}; {:.3f}".format(self.__east, self.__north)

    def __add__(self, p):
        """ Két pont összeadása
            :param p: hozzáadandó pont
            :returns: a két pont összegéből képzett Point2D példányt
        """
        return Point2D(self.__east + p.getEast(), self.__north + p.getNorth())

if __name__ == "__main__":
    """ tesztelő kód az osztályhoz """
    p0 = Point2D()            # pont az origóban
    p1 = Point2D(5)            # pont 5, 0
    p2 = Point2D(north=6)    # pont 0, 6
    p3 = Point2D(-2, 6)        # pont -2, 6
    try:
        p4 = Point2D([12, 5])
    except:
        print("Hibás inicializálás")
    print(p3)
    print(p3.abs())
    print(p3.getEast())
    p3.setEast(99)
    print(p3)
    p3.__east = 4			# nem módosítja a privát változót, de nincs hiba
    print(p3)
