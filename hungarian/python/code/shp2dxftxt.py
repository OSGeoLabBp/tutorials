#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

""" shp attribútum átvitele DXF szövegbe
    pont típusú rétegnél a szöveg a pontba kerül
    törtvonal rétegnél az első pontba
    felület típusú rétegnél a szöveg a centrálisba kerül
    opcionálisan megadható egy oszlop a szöveg szögével és egy szöveg méret
"""
from osgeo import ogr			# shp olvasáshoz
import ezdxf					# dxf iráshoz
from os import (path, unlink)
import sys

if len(sys.argv) < 4:
   print("usage: {} <input_shp> <output_dxf> <txt_column> [rotation_column] [text_height]".format(sys.argv[0]))
   exit(1)

# input réteg
shpfile = sys.argv[1]
if not path.exists(shpfile):
   print("Shape fájlt nem találom")
   exit(2)

# input shape megnyitása
inDriver = ogr.GetDriverByName("ESRI Shapefile")
inDataSource = inDriver.Open(shpfile, 0)
inLayer = inDataSource.GetLayer()

# output dxf file
dxffile = sys.argv[2]
dxf = ezdxf.new(dxfversion='AC1015') # AutoCAD R2000
if path.exists(dxffile):
    unlink(dxffile)
modelSpace = dxf.modelspace()
col = sys.argv[3]        # oszlopnév a felirathoz

rot = 0                  # alapértelmezett szövegirány 0 fok
if len(sys.argv) > 4:
    rotcol = sys.argv[4]

h = 1                    # alapértelmezett szöveg magasság
if len(sys.argv) > 5:
    h = float(sys.argv[5])

# térképi elemek feldolgozása
for feature in inLayer:
    geom = feature.GetGeometryRef()
    if geom.GetGeometryName() == "POLYGON":
        pp = geom.Centroid()    # szöveg a centrálisba
        p = (pp.GetX(), pp.GetY(), pp.GetZ())
    else:
        p = geom.GetPoint(0)   # szöveg az első pontba
    label = feature.GetField(col)
    if len(sys.argv) > 4:
        rot = feature.GetField(rotcol)
    modelSpace.add_text(label, \
        dxfattribs={'height': h, 'rotation': rot}).set_pos(p)

dxf.saveas(dxffile)
