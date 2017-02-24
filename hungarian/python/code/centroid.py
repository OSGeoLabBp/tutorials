#!/usr/bin/env python
""" calculate internal point for polygon 
"""
from sys import argv
from os import path
from osgeo import ogr
from osgeo import osr

if len(argv) < 2:
    print "usage: centroid.py polygon.shp"
    exit(-1)
    #filename = "megye.shp"
else:
    filename = argv[1]
shapefile = ogr.Open(filename)
if not shapefile:
    print "Can't open shapefile: " + filename
    exit(-2)
layer = shapefile.GetLayer(0)
# create output point shapefile
oname = path.splitext(filename)[0] + "_cen.shp"
driver = ogr.GetDriverByName("ESRI Shapefile")
data_source = driver.CreateDataSource(oname)
# set up projection
srs = osr.SpatialReference()
srs.ImportFromEPSG(23700)
# create output layer
odriver = ogr.GetDriverByName("ESRI Shapefile")
# Remove output shapefile if it already exists
if path.exists(oname):
    odriver.DeleteDataSource(oname)

olayer = data_source.CreateLayer("0", srs, ogr.wkbPoint)
# create output field
field_name = ogr.FieldDefn("Nev", ogr.OFTString)
field_name.SetWidth(25)
olayer.CreateField(field_name)

# for all features in input
for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    name = feature.GetField("Nev")
    geometry = feature.GetGeometryRef()
    # attribute and gemetry to output layer
    ofeature = ogr.Feature(olayer.GetLayerDefn())
    ofeature.SetField("Nev", name)
    ofeature.SetGeometry(geometry.Centroid())
    olayer.CreateFeature(ofeature)
# Save and close the data source
data_source = None
