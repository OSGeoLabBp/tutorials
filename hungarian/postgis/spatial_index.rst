Térbeli indexek
===============

**Postgis 3.0**

Összeállította: dr. Siki Zoltán

A PostGIS az úgynevezett GIST indexeket használja a geometria típusú mezőkre.
Az index a geometria minimális befoglaló téglalapja (MBR) alapján épül fel.
Sok PostGIS függvény automatikusan használja a térbeli indexet az elemek gyors 
szűrésére (pl. ST_Contains, ST_Intersects, ST_DWithin, stb.). Bizonyos esetekben
amikor nem használná a PostGIS függvény a térbeli indexet (ilyen például az
ST_Relate), akkor a befoglaló téglalappal dolgozó operátorokkal (pl. &&)
kikényszeríthetjük azt.

A térbeli indexek hatékonyság növelő hatását két táblával mutatjuk be.

* admin8 - magyarországi települések határa (forrás OSM), 3174 felület
* randp - véletlenszerű pontok, településenként 5, 15870 pont

Beleesés és tartalmazás
-----------------------

Először térbeli indexek nélkül próbáljuk meg összekapcsolni a két táblát 
hogy az egyes település felületekbe eső pontokat összeszámoljuk:

.. code:: sql

    SELECT a.id, count(b.*) as total
      FROM admin8 a INNER JOIN randp b ON ST_Intersects(a.geom, b.geom)
      GROUP by a.id;

A fenti lekérdezés végrehajtása egy percet is igénybe vehet a gépünk
erőforrásainak függvényében. Ha belegondolunk, hogy a fenti lekérdezés
a pont a felületben típusú problémát több mint 50 milliószor (3174 * 15870)
oldja meg, nem is tűnik olyan soknak.

Az EXPLAIN ANALYZE paranccsal megvizsgálhatjuk, hogy milyen stratégiát 
használ a Postgres a lekérdezés megoldásánál:

.. code:: sql

    EXPLAIN ANALYZE
        SELECT a.id, count(b.*) as total
          FROM admin8 a INNER JOIN randp b ON ST_Intersects(a.geom, b.geom)
          GROUP by a.id;

A fenti parancs eredménye egy hosszab lista, mely a lekérdezés végrehajtásának 
lépéseit és az azok végrehajtásának becsült idejét tartalmazza.

.. code:: 

                                                                     QUERY PLAN
    ----------------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=0.28..1259916563.06 rows=3174 width=12) (actual time=121.185..29906.204 rows=3174 loops=1)
       Group Key: a.id
       ->  Nested Loop  (cost=0.28..1259915556.87 rows=194889 width=84) (actual time=113.068..29903.742 rows=15870 loops=1)
             Join Filter: st_intersects(a.geom, b.geom)
             Rows Removed by Join Filter: 50355510
             ->  Index Scan using admin8_pkey on admin8 a  (cost=0.28..1035.25 rows=3174 width=2180) (actual time=0.041..2.404 rows=3174 loops=1)
             ->  Materialize  (cost=0.00..419.05 rows=15870 width=112) (actual time=0.036..0.649 rows=15870 loops=3174)
                   ->  Seq Scan on randp b  (cost=0.00..339.70 rows=15870 width=112) (actual time=113.009..115.896 rows=15870 loops=1)
     Planning Time: 0.916 ms
     JIT:
       Functions: 11
       Options: Inlining true, Optimization true, Expressions true, Deforming true
       Timing: Generation 4.153 ms, Inlining 18.163 ms, Optimization 67.979 ms, Emission 26.727 ms, Total 117.022 ms
     Execution Time: 29910.797 ms

A fenti végrehajtási tervből láthatjuk, hogy közel 30 másodpercig tart majd a 
lekérdezés végrehajtása. Egymásba ágyazott ciklusokkal (Nested Loop) dolgozik
az adatbázis-kezelő és a *randp* táblán szekvenciálisan megy végig a belső
ciklusban. Ez az ami nagyon megnöveli a végrehajtási időt. Vegyük észre azt
is, hogy a két tábla összekapcsolása során több mint 50 milliószor az 
összekapcsolási feltétel nem teljesül (Rows Removed by Join Filter).

.. note::

    Az **EXPLAIN** parancsot az **ANALYZE** nélkül is használhatjuk, 
    de akkor a futási időkről nem kapunk tájékoztatást, csak a
    végrehajtási tervet látjuk. Ennek végrehajtása viszont
    sokkal gyorsabb

Próbáljunk gyorsítani a lekérdezés végrehajtási sebességén térbeli index
létrehozásával a *randp* táblára.

.. code:: sql

    CREATE INDEX randp_geom ON randp USING GIST(geom);

Ezután futtassuk újra a korábbi **EXPLAIN ANALYZE** parancsunkat.

.. code:: 

                                                                      QUERY PLAN                                                                  
    ----------------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=0.56..162936.85 rows=3174 width=12) (actual time=10.559..210.614 rows=3174 loops=1)
       Group Key: a.id
       ->  Nested Loop  (cost=0.56..161930.67 rows=194889 width=84) (actual time=10.476..208.473 rows=15870 loops=1)
             ->  Index Scan using admin8_pkey on admin8 a  (cost=0.28..1035.25 rows=3174 width=2180) (actual time=0.021..1.867 rows=3174 loops=1)
             ->  Index Scan using randp_geom on randp b  (cost=0.28..50.67 rows=2 width=112) (actual time=0.039..0.060 rows=5 loops=3174)
                   Index Cond: (geom && a.geom)
                   Filter: st_intersects(a.geom, geom)
                   Rows Removed by Filter: 5
     Planning Time: 0.503 ms
     JIT:
       Functions: 12
       Options: Inlining false, Optimization false, Expressions true, Deforming true
       Timing: Generation 1.995 ms, Inlining 0.000 ms, Optimization 0.621 ms, Emission 9.563 ms, Total 12.179 ms
     Execution Time: 212.825 ms

A lekérdezés futási ideje kevesebb mint tizedére esett vissza. Vegyük észre,
hogy a *randp* táblában a szekvenciális keresés helyett a térbeli index
alapján történik a keresés. Mi történne, ha az *ST\_Intersects* (metsződik) függvény helyett 
az *ST\_Contains* (tartalmaz) függvényt használnánk? Hasonlóan hatékony megoldást
kapnánk? Próbálja ki!

.. note::

    Figyelem, ha többször lefuttatja ugyanazt az **EXPLAIN** parancsot kis
    mértékben eltérő időeredményeket kaphat.

Nézzünk meg egy másik esetet is, amikor az *ST\_Within* (beleesik) függvényt alkalmazzuk
a két geometria vizsgálatára.

.. code:: sql

    EXPLAIN ANALYZE
        SELECT a.id, count(b.*) as total
          FROM admin8 a INNER JOIN randp b ON ST_Within(b.geom, a.geom)
          GROUP by a.id;

Milyen változást jelent ez? A két egymásba ágyazott ciklust felcseréljük, nem
azt vizsgáljuk mindel felületre, hogy a pont beleesik-e, hanem minden
pontra megnézzük, hogy melyik felületbe esik. Azt várhatjuk, hogy a
lekérdezés végrehajtása lelassul mivel a felületekre nincs térbeli indexünk.

.. code:: 

                                                                      QUERY PLAN
    ----------------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=0.56..1274614.48 rows=3174 width=12) (actual time=134.216..292.596 rows=3174 loops=1)
       Group Key: a.id
       ->  Nested Loop  (cost=0.56..1273608.30 rows=194889 width=84) (actual time=134.162..291.123 rows=15870 loops=1)
             ->  Index Scan using admin8_pkey on admin8 a  (cost=0.28..1035.25 rows=3174 width=2180) (actual time=0.020..1.095 rows=3174 loops=1)
             ->  Index Scan using randp_geom on randp b  (cost=0.28..400.92 rows=2 width=112) (actual time=0.031..0.048 rows=5 loops=3174)
                   Index Cond: (geom @ a.geom)
                   Filter: st_within(geom, a.geom)
                   Rows Removed by Filter: 5
     Planning Time: 1.267 ms
     JIT:
       Functions: 12
       Options: Inlining true, Optimization true, Expressions true, Deforming true
       Timing: Generation 3.401 ms, Inlining 41.325 ms, Optimization 63.922 ms, Emission 28.714 ms, Total 137.363 ms
     Execution Time: 296.276 ms

Nem a lassult a lekérdezésünk a várakozásunkkal ellentétben, mert a Postgres lekérdezés
optimalizálója kitalálta, hogy a két ciklus felcserélésével hatékonyabbá
válik a végrehajtás.

Szomszédosság
-------------

Keressük meg, hogy a települések hány másik településsel határosak.
Ehhez az **ST_Touches** függvényt használhatjuk.

.. code:: sql

    SELECT a.name, count(b.*) as szomszed
        FROM admin8 a INNER JOIN admin8 b ON ST_Touches(a.geom, b.geom)
        GROUP BY a.name;

Ez a lekérdezés lassú, nézzük meg a Postgres végrehajtási tervét!

.. code:: sql

    EXPLAIN ANALYZE
        SELECT a.name, count(b.*) as szomszed
            FROM admin8 a INNER JOIN admin8 b ON ST_Touches(a.geom, b.geom)
            GROUP BY a.name;

.. code::

                                                                 QUERY PLAN
    -------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=254789772.05..254790098.01 rows=3155 width=18) (actual time=18872.504..18894.372 rows=3155 loops=1)
       Group Key: a.name
       ->  Sort  (cost=254789772.05..254789870.19 rows=39254 width=2226) (actual time=18872.480..18891.202 rows=18530 loops=1)
             Sort Key: a.name
             Sort Method: external merge  Disk: 42232kB
             ->  Nested Loop  (cost=0.00..254711099.87 rows=39254 width=2226) (actual time=133.840..18810.802 rows=18530 loops=1)
                   Join Filter: st_touches(a.geom, b.geom)
                   Rows Removed by Join Filter: 10055746
                   ->  Seq Scan on admin8 b  (cost=0.00..898.74 rows=3174 width=4392) (actual time=133.211..138.996 rows=3174 loops=1)
                   ->  Materialize  (cost=0.00..1773.61 rows=3174 width=2186) (actual time=0.001..1.164 rows=3174 loops=3174)
                         ->  Seq Scan on admin8 a  (cost=0.00..898.74 rows=3174 width=2186) (actual time=0.009..0.972 rows=3174 loops=1)
     Planning Time: 0.271 ms
     JIT:
       Functions: 13
       Options: Inlining true, Optimization true, Expressions true, Deforming true
       Timing: Generation 2.851 ms, Inlining 17.655 ms, Optimization 77.896 ms, Emission 37.459 ms, Total 135.860 ms
     Execution Time: 18903.954 ms


Láthatjuk, hogy megint szekvenciális keresés van a belső ciklusban és
közel 20 másodpercig tart a lekérdezés végrehajtása. Az *admin8*
rétegre még nem készítettünk térbeli indexet. Tegyük meg ezt és
vizsgáljuk a hatását.

.. code:: sql

    CREATE INDEX admin8_geom ON admin8 USING GIST(geom);

Futassuk újra a lekérdezésünk elemzését.

.. code::

                                                                     QUERY PLAN                                                                   
    -----------------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=163016.38..163342.33 rows=3155 width=18) (actual time=4117.587..4134.275 rows=3155 loops=1)
       Group Key: a.name
       ->  Sort  (cost=163016.38..163114.51 rows=39254 width=2226) (actual time=4117.566..4131.705 rows=18530 loops=1)
             Sort Key: a.name
             Sort Method: external merge  Disk: 42216kB
             ->  Nested Loop  (cost=0.15..84344.19 rows=39254 width=2226) (actual time=60.049..4073.381 rows=18530 loops=1)
                   ->  Seq Scan on admin8 a  (cost=0.00..898.74 rows=3174 width=2186) (actual time=0.013..0.838 rows=3174 loops=1)
                   ->  Index Scan using admin8_geom on admin8 b  (cost=0.15..26.28 rows=1 width=4392) (actual time=0.179..1.263 rows=6 loops=3174)
                         Index Cond: (geom && a.geom)
                         Filter: st_touches(a.geom, geom)
                         Rows Removed by Filter: 2
     Planning Time: 5.385 ms
     JIT:
       Functions: 14
       Options: Inlining false, Optimization false, Expressions true, Deforming true
       Timing: Generation 4.641 ms, Inlining 0.000 ms, Optimization 11.754 ms, Emission 42.955 ms, Total 59.350 ms
     Execution Time: 4274.048 ms

Az index közel negyedére csökkentette a lekérdezés végrehajtásának idejét.
A névre történő csoportképzés miatt egy rendezés szerepel a végrehajtási terve elején. Ezt megspórolhatjuk, ha egy indexet hozunk létre a település névre (*name* oszlop).

.. code:: sql

    CREATE INDEX admin8_name ON admin8(name);

.. code:: 

                                                                      QUERY PLAN
    ----------------------------------------------------------------------------------------------------------------------------------------------
     GroupAggregate  (cost=0.43..87243.87 rows=3155 width=18) (actual time=5.674..4002.998 rows=3155 loops=1)
       Group Key: a.name
       ->  Nested Loop  (cost=0.43..87016.05 rows=39254 width=2226) (actual time=0.749..3996.657 rows=18530 loops=1)
             ->  Index Scan using admin8_name on admin8 a  (cost=0.28..3570.60 rows=3174 width=2186) (actual time=0.136..2.426 rows=3174 loops=1)
             ->  Index Scan using admin8_geom on admin8 b  (cost=0.15..26.28 rows=1 width=4392) (actual time=0.177..1.256 rows=6 loops=3174)
                   Index Cond: (geom && a.geom)
                   Filter: st_touches(a.geom, geom)
                   Rows Removed by Filter: 2
     Planning Time: 1.196 ms
     Execution Time: 4003.326 ms

Ezzel az index-szel már csak kisebb gyorsítást tudtunk elérni. 
