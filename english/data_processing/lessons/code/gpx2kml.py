import sys
from os import path
from osgeo import ogr
"""
    convert gpx files into kml
    usage: python gpx2kml input.gpx input1.gpx ...
        python gpx2kml *.gpx
"""
inDriver = ogr.GetDriverByName('GPX')       # get ogr driver for gpx files
if inDriver is None:
    print('GPX drive not found')
    sys.exit()
outDriver = ogr.GetDriverByName('KML')      # get ogr drive for kml files
if outDriver is None:
    print('KML drive not found')
    sys.exit()
for inName in sys.argv[1:]:                 # go through input files
    src = inDriver.Open(inName, 0)          # open for read
    outName = path.splitext(inName)[0] + '.kml'
    if path.exists(outName):                # ogr can't overwrite output
        outDriver.DeleteDataSource(outName) # delete !!!! danger
    dst = outDriver.CopyDataSource(src, outName)    # copy to destination
