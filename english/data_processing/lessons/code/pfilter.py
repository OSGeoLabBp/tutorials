#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" filter point file
"""

import sys
import re

def GetNext(fp, separator=';'):
    """ get next line from file and parse """
    buf = fp.readline()
    res = tuple()   # empty tuple marks invalid input line
    if buf:     # None returned on end of file
        fields = [f.strip() for f in buf.strip().split(separator) if len(f)]
        if len(fields) > 2:
            try:
                res = fields[0], [float(f) for f in fields[1:]]
            except Exception:
                pass
        return res
    return None

def GetCoo(fn, sep=';'):
    """ load coordinates into a dictionary
    """
    fp = open(fn, 'r')
    plist = {}
    l = GetNext(fp, sep)
    while l is not None:
        if len(l):
            plist[l[0]] = l[1]
        l = GetNext(fp, sep)
    return plist

def Filter(pl, pattern):
    """ filter points 
    """
    pat = re.compile(pattern)
    res = {}
    for key in pl:
        if pat.search(key):
            #res[key] = pl[key]   # !!!! danger !!!!
            res[key] = pl[key][:]
    return res

def Area(pl, ps):
    """ calculate area of points given in ps by name
    """
    n = len(ps)
    are = 0
    for i in range(n):
        j = (i + 1) % n
        if ps[i] in pl and ps[j] in pl:
           are += (pl[ps[i]][0] + pl[ps[j]][0]) * (pl[ps[i]][1] - pl[ps[j]][1])
    return are / 2

if __name__ == '__main__':
    """ simple test """
    pp = GetCoo('labor.csv', ';')
    print(Filter(pp, '^1'))
    print(Area(pp, ['501', '507', '509', '515']))
