Permanens GPS állomás adatainak letöltése IGS ftp szerverről, python scripttel
==============================================================================
*szerző: Takács Bence (takacs.bence@epito.bme.hu), BME Általános- és Felsőgeodézia Tanszék. utolsó módosítás: 2016. január 7.*

Korábban arról írtunk, hogyan lehet egy permanens állomás nyers mérési adatait letölteni: https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/gps/gps_adatok_letoltese.rst.
Rövid írásunk végén mutattunk egy shell scriptet, amelynek segítségével linux környezetben parancssorból letölthetünk és kitömöríthetünk mérési és navigációs állományokat. Ebben az írásban mindezt python script segítségével oldjuk meg. A python script egyik előnye, hogy lényegében bármilyen operációs rendszeren futtatható. Python alapismerteket feltételezzük, pythonban teljesen kezdőknek javasoljuk: http://www.geod.bme.hu/gis/python/python_oktato.pdf

**1. lépés:** előző nap dátuma::
from datetime import date, timedelta
yesterday = date.today() - timedelta(1)
doy = yesterday.strftime('%j')
year = yesterday.strftime('%Y')
year2 = yesterday.strftime('%y')
