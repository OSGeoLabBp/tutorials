Adminisztratív határok OSM-ből
==============================

GDAL/OGR 3.0

Összeállította: Siki Zoltán

Ebben a rövid példában az mutatjuk be, hogy az OpenStreetMap Magyarországra 
leszűrt állományból hogyan készíthetünk további szűréseket hatékonyan a 
parancssorból. A download.geofabric.de oldalról országokra szétszedett 
állományokat tölthetünk le, melyeket hetente frissítenek. Célunk, hogy a 
parancssorba beírható parancsokat használjunk és így teljesen automatizáljuk
a folyamatot, az egymásutáni parancsok egy parancsfájba beírva akár 
rendszeresen automatizáltan elindítható a gépen.

Az állomány letöltését is már a parancsorból végezzük el a **wget** 
programmal. Ehhez egyszer el kell látogatnunk a kedvelt böngésző
programunkkal a GeoFabrik oldalára, a hogy kérdéses állomány linkjét 
beszerezzük.

.. code:: html

       https://download.geofabrik.de/europe/hungary-latest.osm.pbf

A dokumentum készítésének idejében a *pbf* fájl mérete ~170MB. 
A fájl letöltéséhez a **wget** prarancsot használjuk, melyet Windows
parancsablakban is használhatunk, nem csak Linux-on:

.. code:: bash

        wget -q -t 10 https://download.geofabrik.de/europe/hungary-latest.osm.pbf

A *-q* kapcsoló csendes üzemmódot jelent, az üzenetek nem jelennek meg, ezt
azért használjuk, mert az automatizálás a célunk, nem ül majd a gép előtt senki,aki elolvasná az üzeneteket. A *-t 10* beállítás sikertelen letöltés esetére 10 
ismételt próbálkozást tesz lehetővé. amennyiben más névvel szeretnék a 
gépünkre menteni a fájlt, akkor azt a *-O fájl_név* alakban adhatjuk meg.

Először nézük meg, hogy milyen rétegek szerepelnek a pbf fájlban.
Erre a *ogrinfo* programot használjuk.

.. code:: bash

        ogrinfo hungary-latest.osm.pbf

A fenti parancs néhány soros információt ad a fájlról:

.. code:: bash

        INFO: Open of `hungary-latest.osm.pbf'
              using driver `OSM' successful.
        1: points (Point)
        2: lines (Line String)
        3: multilinestrings (Multi Line String)
        4: multipolygons (Multi Polygon)
        5: other_relations (Geometry Collection)

A fenti lista azt jelenti, hogy a *pbf* fájlban öt réteg van. Azért kapjuk
ezt a kis számot, mert az *OSM* adatszervezése nem a térinformatika 
hagyományos rétegei szerint történik, az *ogr* geometria típus alapján
sorolja rétegekbe az elemeket.

Először a település határokra szűrjűk az állományt. Ehhez egy kicsit
ismernünk kell az *OSM* adatokat. Az egyes geometriai elemekhez tegeket 
fűzhetünk. Egy elemhez tetszőleges számú teg tartozhat (egy tag egy névből
és egy értékből áll). A településhatárokat az *admin_level* teg *8*-as 
értéke jelöli. Nézzük meg, hogy hány ilyen térképi elem (multipolygon) van az
állományban. Ehhez az *ogrinfo* parancsot SQL lekérdezéssel kombináljuk.

.. code:: bash

        ogrinfo -SQL "SELECT count(*) FROM multipolygons WHERE admin_level='8'" hungary-latest.osm.pbf

A fenti paranccsal az *admin_level* tegben *8* értéket tartalmazó elemek 
számát kérdeztük le a multipolygons rétegből.

.. code:: bash

        Had to open data source read-only.
        INFO: Open of `hungary-latest.osm.pbf'
              using driver `OSM' successful.

        Layer name: multipolygons
        Geometry: None
        Feature Count: 1
        Layer SRS WKT:
        (unknown)
        COUNT_*: Integer (0.0)
        OGRFeature(multipolygons):0
        COUNT_* (Integer) = 3220

3220 településhatárt tartalmaz a letöltött állomány (a KSH 2014-es adatai 
szerint 3154 település volt).

Ezek után készítsünk egy új GeoPackage állományt a településhatárokból EOV vetületben.

.. code:: bash

        ogr2ogr -overwrite -t_srs EPSG:23700 \
          -sql "SELECT * FROM multipolygons WHERE admin_level='8'" \
          -f "GPKG" telepulesek.gpkg hungary-latest.osm.pbf

Nyissuk meg az így létrehozott Geopackage réteget a QGIS-sel. Az állományt
szemlélve észrevehetjük, hogy van több határon túli település illetve
egyházközségek is megjelennek az állományban pl. Budapest XXII. kerületében.
Ezek a nem várt terület elemek egyrészt a GeoFabrik szűrésének lehet a hibája,
másrészt az egyes önkéntes adatfeltöltők tájékozatlansága. További
adminisztratív határokat is kinyerhetünk az OSM állományból.

+-------------+------------------------------------------+
| admin_level | leírás                                   |
+-------------+------------------------------------------+
|      2      | Országhatár                              |
+-------------+------------------------------------------+
|      5      | Régiók (7 darab) NUTS 2                  |
+-------------+------------------------------------------+
|      6      | Megyék + Budapest (20 darab) NUTS 3      |
+-------------+------------------------------------------+
|      7      | Járások (175 darab) LAU 1                |
+-------------+------------------------------------------+
|      8      | Települések (3174 darab) LAU 2           |
+-------------+------------------------------------------+

Az OSM tartalmából számos további hasznos adatokat szűrhetünk le. A következő
példa az épületeket (~1.2 millió) szedi ki egy Gepackage adatbázisba:

.. code:: bash

        ogr2ogr -overwrite -t_srs EPSG:23700 \
          -sql "SELECT * FROM multipolygons WHERE building is not NULL" \
          -f "GPKG" buildings.gpkg hungary-latest.osm.pbf

A lustábbak rögtön kezdhetik a https://data2.openstreetmap.hu/hatarok/index.php
oldalon, ahonnan több adminisztratív szintre kész shape fájlokat tölthetnek le.

2020. április 28.
