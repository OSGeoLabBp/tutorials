#! /usr/bin/python
# -*- coding: UTF-8 -*-

""" sample code for demonstrating shapely functionality """
import shapely
import shapely.wkt
import os
import sys
from osgeo import ogr

if len(sys.argv) < 2:
    print "Usage: {} <shp_file> [buffer_distance]".format(sys.argv[0])
    exit(1)

shapename = sys.argv[1]
shapefile = ogr.Open(shapename)       # input point shape
if shapefile is None:
    print "shape file not found"
    exit(1)
layer = shapefile.GetLayer(0)

if len(sys.argv) < 3:
    bufdist = 30000                 # default buffer distance 30 km
else:
    try:
        bufdist = float(sys.argv[2])
    except ValueError:
        print "Illegal buffer distance parameter"
        exir(1)
driver = ogr.GetDriverByName("ESRI Shapefile")

outshp = os.path.splitext(shapename)[0] + "_buf.shp"
if os.path.exists(outshp):              # remove ouput shape
    driver.DeleteDataSource(outshp)
dstFile = driver.CreateDataSource(outshp) # create output shape
dstLayer = dstFile.CreateLayer("layer", geom_type=ogr.wkbPolygon)
field = ogr.FieldDefn("id", ogr.OFTInteger)     # create output field
dstLayer.CreateField(field)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)       # get point from input
    geometry = feature.GetGeometryRef()
    wkt = geometry.ExportToWkt()        # change to wkt format
    p = shapely.wkt.loads(wkt)          # convert to shapely geom
    pb = p.buffer(bufdist)              # buffer
    wktb = shapely.wkt.dumps(pb)        # export to wkt
    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(ogr.CreateGeometryFromWkt(wktb))
    feature.SetField("id", i)           # set id
    dstLayer.CreateFeature(feature)

dstFile.Destroy()                       # close output
