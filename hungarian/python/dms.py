import math

def dms2rad(dms):
    """
        dms to radian
        input ddd-mm-ss
        return value in radian
    """
    items = dms.split('-')
    return math.radians(float(items[0])+float(items[1])/60.0+float(items[2])/3600.0)
