from osgeo import gdal
from gdalconst import GA_ReadOnly
import struct
from sys import argv

if len(argv) < 3:
	print("Használat: {} dtm_tiff magasság".format(argv[0]))
	exit(1)
data = gdal.Open(argv[1], GA_ReadOnly) # DTM megnyitása
if data is None:
    print("TIFF nyitási hiba")
    exit(2)
try:
    height = float(argv[2])
except ValueError:
    print("Hibás magasság")
    exit(3)
geotr = data.GetGeoTransform()
band = data.GetRasterBand(1)     		# első sáv a képből
no_data = band.GetNoDataValue()			# nincs adat érték lekérdezése
fmt = "<" + ("f" * band.XSize)   		# formátum 1 sorhoz, 32 bit valós
pixel_area = abs(geotr[1] * geotr[5])	# egy pixel területe
area = 0.0                       		# terület összegzéshez

for y in range(band.YSize):				# minden pixel sorra
    scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
    values = struct.unpack(fmt, scanline)	# magasságok beolvasása és listává alakítása
    for value in values:
        if value < height and value != no_data:
            area += pixel_area
print(area)
