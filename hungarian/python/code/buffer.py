#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from osgeo import ogr
import shapely.wkt
import os.path

shapefile = ogr.Open("varos.shp")       # input pont shape
if shapefile is None:
	print("Nem találom a varos.shp fájlt")
	exit(1)
layer = shapefile.GetLayer(0)

driver = ogr.GetDriverByName("ESRI Shapefile")
outshp = "varosb.shp"
if os.path.exists(outshp):              # létező output törlése
    driver.DeleteDataSource(outshp)
dstFile = driver.CreateDataSource("varosb.shp") # output shape létrehozása
dstLayer = dstFile.CreateLayer("layer", geom_type=ogr.wkbPolygon)
field = ogr.FieldDefn("id", ogr.OFTInteger)     # id mező létrehozása
dstLayer.CreateField(field)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)       # pont az inputból
    geometry = feature.GetGeometryRef()
    wkt = geometry.ExportToWkt()        # átalakítás wkt formátumba
    p = shapely.wkt.loads(wkt)          # átalakítás shapely geometriába
    pb = p.buffer(30000)                # 30 km buffer
    wktb = shapely.wkt.dumps(pb)        # export wkt-ba
    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(ogr.CreateGeometryFromWkt(wktb))
    feature.SetField("id", i)           # id
    dstLayer.CreateFeature(feature)

dstFile.Destroy()                       # mentés és output lezárás
