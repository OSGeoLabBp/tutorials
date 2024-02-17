Tér-idő adatok kinyerése GPX fájlokból
======================================

A tér-idő adattáblák legegyszerűbb esete amikor pontszerű adatokhoz 
rendelünk egy időpontot. Jellemzően ez egy vagy több mozgó 
objektum mozgását leíró adatok. Ilyen adatokat többféle 
eszközzel gyűjthetünk, mi egy Garmin szabadidős GNSS vevőt használunk,
mely GPX formátumban állítja elő az adatokat. A GPX egy nemzetközi 
szabvány, mely XML formátumban tartalmazza az adatainkat.

A GPX fájlok szerkezete
-----------------------

A GPX fájlok egy egszerű szövegszerkesztő programmal is megtekinthetők.
Például ebben lecképen használt GPX fájl eleje így néz ki:

.. code::

    <?xml version="1.0" encoding="UTF-8" standalone="no" ?><gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="Dakota 20" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"><metadata><link href="http://www.garmin.com"><text>Garmin International</text></link><time>2022-08-22T14:09:04Z</time></metadata><trk><name>Current Track: 05 AUG 2022 09:01</name><extensions><gpxx:TrackExtension>

Használt szoftverek
-------------------

A munka során a PosgreSQL adatbáziskezelőt és a PostGIS térinformatikai 
bővítményt használjuk. Emellet az adatok konvertálását a GDAL/OGR
segédprogramokat használjuk, az adatok megjelenítésére a QGIS
programot használjuk. A PostgreSQL és PostGIS telepítéséről egy
`külön lecke <https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/postgis/pg_inst.rst>`_
készült. Windows operációs rendszeren a QGIS és a GDAL segédprogramok telepítésére
az `OSGeo4W <https://trac.osgeo.org/osgeo4w/>`_ tepelítő használata a legcélszerűbb.

Adatok
------

Egy kerékpárral `rögzített útvonalat <https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/postgis/data/god_2022.gpx>`_ biztosítunk a részletezett folyamat
bemutatására, de tetszőleges GPX fájl használható, melyben rögzített
nyom (track) van.

A GPX fájlok szerkezete
-----------------------

A GPX fájlok egy egszerű szövegszerkesztő programmal is megtekinthetők.
Például ebben leckében használt GPX fájl eleje így néz ki:

.. code::

    <?xml version="1.0" encoding="UTF-8" standalone="no" ?><gpx xmlns="http://www.topografix.com/GPX/1/1" xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3" xmlns:wptx1="http://www.garmin.com/xmlschemas/WaypointExtension/v1" xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1" creator="Dakota 20" version="1.1" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www8.garmin.com/xmlschemas/GpxExtensionsv3.xsd http://www.garmin.com/xmlschemas/WaypointExtension/v1 http://www8.garmin.com/xmlschemas/WaypointExtensionv1.xsd http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"><metadata><link href="http://www.garmin.com"><text>Garmin International</text></link><time>2022-08-22T14:09:04Z</time></metadata><trk><name>Current Track: 05 AUG 2022 09:01</name><extensions><gpxx:TrackExtension>

Egy gpx fájlban található rétegeket az *ogrinfo* segédprogrammal 
tekinthetjük meg (ez a GDAL/OGR segédprogramokkal települ).

.. code:: 

    ogrinfo god_2022.gpx
    INFO: Open of `god_2022.gpx'
      using driver `GPX' successful.
    1: waypoints (Point)
    2: routes (Line String)
    3: tracks (Multi Line String)
    4: route_points (Point)
    5: track_points (Point)

Nem minden réteg található meg minden gpx fájlban. Az egyes 
rétegek a következő adatokat tartalmazzák (a rétegnév
mögötti zárójelbe tett információ az adat geometriai típusára utal):

- waypoints (Points) - menetközben manuálisan rögzített pontok, időponttal
- routes (Line String) - manuálisan létrehozott útvonalak
- tracks (Line String) - a GNSS eszköz mozgása közben automatikusan rögzített útvonal
- route_points (Point) - a manuálisan létrehozott útvonalak töréspontjai
- track_points (Point) - az automatikusan rögzített útvonalak töréspontjai időpontokkal

A fentiek közül a track_points réteget használjuk majd.
Nézzük meg ennek a tartalmaát is!

.. code::

    ogrinfo god_2022.gpx track_points
    INFO: Open of `god_2022.gpx'
      using driver `GPX' successful.

    Layer name: track_points
    Geometry: Point
    Feature Count: 3651
    Extent: (19.038352, 47.445059) - (19.131795, 47.680852)
    Layer SRS WKT:
    GEOGCRS["WGS 84",
        DATUM["World Geodetic System 1984",
            ELLIPSOID["WGS 84",6378137,298.257223563,
                LENGTHUNIT["metre",1]]],
        PRIMEM["Greenwich",0,
            ANGLEUNIT["degree",0.0174532925199433]],
        CS[ellipsoidal,2],
            AXIS["geodetic latitude (Lat)",north,
                ORDER[1],
                ANGLEUNIT["degree",0.0174532925199433]],
            AXIS["geodetic longitude (Lon)",east,
                ORDER[2],
                ANGLEUNIT["degree",0.0174532925199433]],
        ID["EPSG",4326]]
    Data axis to CRS axis mapping: 2,1
    track_fid: Integer (0.0)
    track_seg_id: Integer (0.0)
    track_seg_point_id: Integer (0.0)
    ele: Real (0.0)
    time: DateTime (0.0)
    ... 
    OGRFeature(track_points):0
      track_fid (Integer) = 0
      track_seg_id (Integer) = 0
      track_seg_point_id (Integer) = 0
      ele (Real) = 56.37
      time (DateTime) = 2022/08/05 07:01:02+00
      POINT (19.0417610295 47.4451178312)

    OGRFeature(track_points):1
      track_fid (Integer) = 0
      track_seg_id (Integer) = 0
      track_seg_point_id (Integer) = 1
      ele (Real) = 56.37
      time (DateTime) = 2022/08/05 07:01:03+00
      POINT (19.0417507198 47.4451288115)

    OGRFeature(track_points):2
      track_fid (Integer) = 0
      track_seg_id (Integer) = 0
      track_seg_point_id (Integer) = 2
      ele (Real) = 56.37
      time (DateTime) = 2022/08/05 07:01:08+00
      POINT (19.041764047 47.4450594932)
    ...

A fájl elején a fejléc információból kiolvashatjuk, hogy 3651
pontot tartalmaz, a 4326 EPSG azonosítójú referencia rendszerben
(WGS84). A fejlécből több számunkra lényegtelen sort töröltünk és
a 3651 pontból is csak hármat tartalmaz a fenti lista.

A PostGIS csak ESRI Shape fájlok importjára biztosít lehetőséget,
ezért az attól független *ogr2ogr* segédprogramot használjuk, mely 
több tucat vektoros formátum közötti konverzióra alkalmas. 
Szerencsére ezek között szerepel a PostGIS is.

Előkészítés a PostgreSQL oldalon
--------------------------------

A következőkben feltételezzük, hogy az alapértelmezett adatbázisunkba
telepítettük a *PostGIS* bővítményt a következő paranccsal egy SQL
utasítások bevitelére alkalmas:

.. code::

    CREATE EXTENSION postgis;

Az adatok fogadására egy táblát és szekvenciát kell létrehoznunk.
A szekvenciára azért lesz szükségünk, hogy az egyszerre feltöltött 
gpx adatokat azonos azonosítóval lássuk el és egíidőben mozgó
eszközeink adatait is szét tudjuk választani.

.. code:: SQL

    CREATE SEQUENCE IF NOT EXISTS track;

Majd hozzuk létre a tér-idő adatokat tároló táblánkat:

.. code:: sql

    CREATE TABLE IF NOT EXISTS test (
        tid bigint DEFAULT -1,                -- track unique id generated
        track_seg_point_id integer,           -- point ordinal number
        geom geometry(Point,4326) NOT NULL,   -- point geometry in wgs84
        ele double precision,                 -- elevation
        "time" timestamp with time zone,      -- timestamp of position
        PRIMARY KEY (tid, "time")
    );

A *tid* oszlop tárolja majd az egyes feltöltött nyomokat, az alapértelmezett 
értéke azért -1 mert ezt csak a feltölés után beállítani. Ezután a gpx fájlból
érkező minimális adatok szerepelnek. Az *ogr2ogr* csak azokban az
oszlopoknak az adatait veszi át a gpx fájlból, melynek megfelelő oszlop
szerepel a cél adattábla definíciójában.

A fenti két SQL blokk utasításait összetehetjük egy .sql fájlba,
legyen ez a fájl a *gpx_points2pg.sql*. A parancssorból vagy a
*PgAdmin4* alkalmazásból futtathatjuk az sql szkriptet.

A parancssori futtatás:

.. code::

    psql < gpx_points2pg.sql

A fenti utasítás akkor működik, ha az alapértelmezett felhasználó,
alapértelmezett adatbásis megfelelő és az aktuális gépen fut az
PostgreSQL szerverünk. Különben további kapcsolókat kell
használni. Ezeket a

.. code::

    psql --help

paranccsal nézheti meg.

Adatok betöltése
----------------

Az előkészítés után az adatok betöltése ezután már egyetlen
*ogr2ogr* parancsot kell végrehajtanunk:

.. code::

    ogr2ogr -update -append -f "PostgreSQL"  PG:"host="127.0.0.1" user="xxxxxx" dbname ="xxxxx" password="xxxxxx"" god_2022.gpx  -nln test -sql "Select * From track_points"

A fenti parancsban változtassa meg PG: utáni paramétereket.

A feltöltés után még a *tid* oszlop tartalmát módosítanunk kell.
Erre a következő két SQL utasítást használjuk:

.. code:: sql

    SELECT nextval('track');
    UPDATE test SET tid = currval('track') WHERE tid = -1;

Egy újabb SQL szkript fájlba beírva a fenti két SQL utasítást, 
az előzőhöz hasonlóan futtathatjuk, Sőt a teljes folyamatott 
egyetlen parancsfájlban foglalhatjuk össze:

.. code::

    # creating neccesary database objects
    psql < gpx_points2pg.sql
    # load data to database
    ogr2ogr -update -append -f "PostgreSQL"  PG:"host="127.0.0.1" user="xxxxxx" dbname="xxxxxx" password="xxxxxx"" god_2022.gpx  -nln test -sql "Select * From track_points"
    # fix track id
    psql < gpx_points2pg_post.sql


