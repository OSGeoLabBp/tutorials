import sys
from os import path
from osgeo import ogr

inDriver = ogr.GetDriverByName('GPX')   # get driver for gpx files
if inDriver is None:
    print('GPX drive not found')
    sys.exit()
outDriver = ogr.GetDriverByName('KML')  # get driver for kml files
if outDriver is None:
    print('KML drive not found')
    sys.exit()
for inName in sys.argv[1:]:             # go through input files
    src = inDriver.Open(inName, 0)      # open for read
    outName = path.splitext(inName)[0] + '.kml'
    if path.exists(outName):            # ogr can't overwrite output
        outDriver.DeleteDataSource(outName) # delete !!!! danger
    dst = outDriver.CreateDataSource(outName)   # new output data source
    for i in range(src.GetLayerCount()):    # go through layers of input
        inLayer = src.GetLayerByIndex(i)
        if inLayer.GetFeatureCount():   # copy only non-empty layers
            outLayer = dst.CreateLayer(inLayer.GetName(),
                geom_type=inLayer.GetGeomType())
            for feat in inLayer:        # go through features of input layer
                outLayer.CreateFeature(feat)    # add feature to output layer
    dst = None  # save and close dataset
    scr = None
