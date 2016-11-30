import math
import re

class Angle(object):
    """ class to operate angles
    """

    def __init__(self, v = 0):
        self.val = v

    @staticmethod
    def dms2rad(dms):
        """
            Convert DMS angle (in the form ddd-mm-ss) to radians
            retuns angle in radians
            This static method can be called by the class
            e.g Angle.dms2rad('12-12-12')
        """
        dms = dms.strip()         # remove whitespace
        sign = 1                  # assume positive dms value
        if dms[0] == "-":
            sign = -1
            dms = dms[1:]         # remove sign
        items = re.split('[-/:]', dms, maxsplit=3)  # get list of [ddd, mm, ss]
        while len(items) < 3:     # add missing mins/secs
            items.append('0')
        # change to decimal degree with sign
        return sign * math.radians(float(items[0]) + float(items[1]) / 60.0 +
                            float(items[2]) / 3600.0)

    @staticmethod
    def rad2dms(rad):
        """
            Convert angle in radians to DMS string
            returns dms string e.g '12-12-12'
            This static method can be called by the class
            e.g Angle.rad2dms(3.12345)
        """
        secs = round(abs(rad) * 180.0 / math.pi * 3600)
        mi, sec = divmod(secs, 60)
        deg, mi = divmod(mi, 60)
        deg = int(deg)
        return "%s%d-%02d-%02d" % ("-" if rad < 0 else "", deg, mi, sec)

    def __str__(self):
        """
            convert angle to dms string
            this method is called by print
        """
        return self.rad2dms(self.val)

    def __add__(self, a):
        """
            add two angles
            this method is called by the '+' operator
            __class__ is used to get an instance of the actual class
        """
        return self.__class__(self.val + a.val)

    def __iadd__(self, a):
        """
            increment an angle
            this method is called ba the += operator
        """
        self.val += a.val
        return self

    def __sub__(self, a):
        """
            substract angles
            this method is called by the '-' operator
            __class__ is used to get an instance of the actual class
        """
        return self.__class__(self.val - a.val)

    def __isub__(self, a):
        """
            decrement angle
            this method is called ba the -= operator
        """
        self.val -= a.val
        return self
        
    @property
    def val(self):
        """
            get hidden value of object
        """
        return self._val
    
    @val.setter
    def val(self, v = 0):
        """ set hidden value given in dms or radians
        """
        if isinstance(v, str):
            v = self.dms2rad(v)     # convert dms to radian
        self._val = v               # save value in radian
        return self

    def normalize(self):
        """ shift angle into the 0-2pi interval
        """
        while self.val < 0:
            self.val += 2 * math.pi
        while self.val >= 2 * math.pi:
            self.val -= 2 * math.pi
        return self

class NormalizedAngle(Angle):
    """ normalized angle always in 0, 2pi interval
    """

    @property
    def val(self):
        return self._val

    def __init__(self, val):
        super(NormalizedAngle, self).__init__(val)    # call constructor of parent class

    @val.setter
    def val(self, v = 0):
        """ set value given in dms or radians and shift it into 0,2pi interval
        """
        if isinstance(v, str):
            v = self.dms2rad(v)     # convert dms to radian
        while v < 0:
            v += 2 * math.pi
        while v >= 2 * math.pi:
            v -= 2 * math.pi
        self._val = v
        return self

    def normalize(self):
        """ just overload parent's method
        """
        return self

if __name__ == '__main__':

    a1 = Angle('-12-23-34').normalize()
    print(a1)
    a2 = Angle(math.pi)
    a3 = a1 + a2
    print(a3)
    a1 += Angle('11-11-11')
    print(a1)
    b1 = NormalizedAngle('-12-23-34')
    print(a1-a1)
    print(Angle.rad2dms(0.11111))
