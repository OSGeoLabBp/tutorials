2.5D megjelenítés
=================

QGIS 3.8+

**Összeállította: dr. Siki Zoltán**

A QGIS tematikus megjelenítés egy speciális fajtája a 2.5 nézet. Ezzel 3D-s
hatást tudunk elérni a sima térkép ablakban egy magasság és egy irány
megadásával.

Használjuk az OSM adatokat, melyben az épületek többségéhez a szintek száma
ismert adat. Én a Műegyetek környékét kérdeztem le az OSM adatokból az
*OSMDownloader* modul segítségével. A modul telepítése után egy új eszköz
jelenik meg az eszközeink között, mellyel egy téglalapot jelölhetünk ki az
OSM letöltéséhez. A letöltött adatokat három rétegben (pontok, törtvonalak,
felületek) és három nagyítási szintnek megfelelő tematikával jeleníti meg.
Ezen adatok közül mi csak az épületeket szeretnénk használni, melyek a
felülettel bíró elemek között találhatók.

A pontokat és vonalakat tartalmazó rétegeket kapcsoljuk ki vagy akár el is 
távolíthatjuk a projektünkből.
A felületeket tartalmazó réteget szűkítsük le csak azokra az elemekre, melyre
a *Building* OSM taget beállították, a réteg tulajdonságok ablakban a 
**Forrás** fülön az elemszűréshez írjuk be:

.. code::

    "building" is not NULL

.. image:: images/25d1.png
   :align: center

Ezután a jelrendszer fülön a *Szabály alapú* megjelenítés helyett válasszuk
a *2.5 D* megjelenítést. A magasság mező beállításához az OSM *other_tags*
mezőjéből ki kell nyernünk a szintek számát az egyes épületek magasságának 
beállításához. Egy összetett kifejezéssel először az *other_tags* mezőben 
lévő több adat közül a *regexp_substr* fügvénnyel kivesszük a *building:levels*
mezőt, majd ebből csak a szintek számát őrizzük meg a *replace* fügvénnyel,
végül megszorozzuk egy konstanssal, hogy a szintek számából magasságot kapjunk.

.. code::

    replace(regexp_substr( "other_tags", '(building:levels"=>"[0-9]+)'), 'building:levels"=>"', '') * 0.0001

A használt konstans értéke azért ilyen kicsi, mert az OSM adataink fokokban
vannak. A *Szög* határozza meg, hogy milyen irányból nézzük az épületeket.

A *Bővített* beállítások között állítsuk be a színeket, árnyékot.

.. image:: images/25d2.png
   :align: center

A réteg tulajdonságok ablak bezárása után az épületek térhatású megjelenítését
kapjuk. Háttér rétegként még a QMS modullal az OSM térkép hozzáadtam a 
projekthez.

.. image:: images/25d3.png
   :align: center

Az eredmény ábrán is láthatjuk, hogy nem minden épület emelkedik ki. Ennek
az  az oka, hogy a *building* vagy a *building:level* tag nincs beállítva.
Regisztráljon OSM szerkesztőnek és javítsa a hibákat.

2023. április 11.


