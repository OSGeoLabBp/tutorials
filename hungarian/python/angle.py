import math

def dms2rad(dms):
    """
        dms to radian
        input ddd-mm-ss
        return value in radian
    """
    items = dms.split('-')
    while len(items)<3: 
        items.append('0') 
    return math.radians(float(items[0])+float(items[1])/60.0+float(items[2])/3600.0)

def rad2dms(rad):
    """
		radian to dms
		input rad
		return value in dms
    """
    secs = round(rad*180.0/math.pi*3600.0)
    mi,sec = divmod(secs,60)
    deg,mi = divmod(mi,60)
    deg = int(deg)
    return "%d-%02d-%02d" % (deg,mi,sec)

class Angle(object):
    """
		class to handle angles
    """
    def __init__(self,val=0):
        self.setval(val)
        
    def setval(self,val=0):
        if isinstance(val,str):
            self.val = dms2rad(val)
        else:
            self.val = val

    def __str__(self):
        return rad2dms(self.val)

if __name__== "__main__":
    print (dms2rad('12'))
    print (dms2rad('12-34'))
    print (dms2rad('12-34-56'))
    print (rad2dms(dms2rad('12-23-34')))
    a = Angle('123-31-16')
    print(a)