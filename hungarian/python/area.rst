Python oktatóanyag, az egyszerű algoritmustól az osztályokig
============================================================

Ebben az oktatóanyagban zárt sokszög területének koordinátákból történő 
kiszámítását oldjuk meg többféleképpen. Az egyes megoldások fájljai
megtalálhatók a *code* mappában. A kódok futtathatók Python 2 és 
Python 3 verzióban is.

A probléma
----------

Adott egy zárt sokszög töréspontjainak koordinátáival. Az idom területét az
egyes oldalakhoz tartozó trapézok területének összegzésével számítjuk ki.

.. math::

	{sum(x_{i+1} - x_{i}) * (y_{i+1} + y_{i})} over {2}

A fenti képletben az utolsó pont esetén (i = n) az i+1 az első pontra 
vonatkozik.

A töréspontok koordinátáit tároljuk egy összetett listában. Az egyes pontok 
koordinátáit tegyük egy két elemű listába és ezekből alkossunk egy listát a
zárt idomhoz. A kezdőpont koordinátáját nem kell a lista végén újra megadni.
Az alábbi egy háromszög leírása.

.. code:: Python

	coords = [[1, 1], [3, 1], [2, 2]]


Első változat (area.py)
-----------------------

A trapéz területeket számítsuk ki egyesével egy ciklusban és a részösszegeket
egy változóban összegezzük (area).

.. code:: python

	area = 0.0
	for i in range(len(coords)):
		j = (i + 1) % len(coords)
		area += (coords[j][0] + coords[i][0]) * (coords[j][1] - coords[i][1])
	area /= 2.0
	print(abs(area))

A **len** függvény a lista hosszát adja vissza (azaz a töréspontok számát).
A **range(n)** függvényhívás a egész számok listáját adja vissza nullától
**n-1**-ig. A **%** operátor az osztási maradékot adja, ezzel álítjuk elő,
hogy az utosó pont után az első pontot használja a program. A listák 
indexelése nullától indul (az első elem indexe nulla). A **coords[i]**
egy pont koordinátáit jelenti (két elemű lista), a **coords[i][0]** az 
i-edik pont első koordinátáját jelenti. Az így számított terület negatív is 
lehet, körüljárási iránytól függően, ezért használjuk az **abs** 
(abszolútérték) függvényt.

Második változat (area1.py)
---------------------------

Amennyiben többször szeretnénk megismételni a területszámítást különböző 
zárt sokszögekre, akkor célszerűbb a kódot egy függvénybe tenni.

.. code:: python

	def area(coords):
		""" calculate area of a polygon

			:param coords: vertexes of polygon e.g. [[1, 1], [3, 1], [2, 2]]
			:returns: area of polygon
		"""
		w = 0.0
		for i in range(len(coords)):
			j = (i + 1) % len(coords)
			w += (coords[j][0] + coords[i][0]) * (coords[j][1] - coords[i][1])
		return abs(w) /2.0

A **def** alapszó jelöli a függvény kezdetét, utána a függvény neve és 
zárójelben a paraméterei következnek. A **return** után álló kifejezés
értékét adja vissza a függvény. A függvény használatára itt egy példa:

.. code:: python

	coords0 = [[1, 1], [3, 1], [2, 2]]
	coords = [[634110.62 , 232422.09 ],
		[634108.23, 232365.96],
		[634066.13, 232378.12],
		[634062.95, 232457.58],
		[634111.68, 232454.93],
		[634110.62, 232422.09]]
	print(area(coords0))
	print(area(coords))

Harmadik változat (area2.py)
----------------------------

A Python az objektum orientált programozást is támogatja. Készítsünk egy
**Polygon** objektumot.

.. code:: python

	class Polygon(object):
		""" Polygon class to store border and calculate area
			:param coords: list of lists of coordinate pairs [[1, 2], [3, 5], [2, 6]]
		"""
		def __init__(self, coords):
			self.coords = coords

		def area(self):
			""" Calculate the area of polygon from the coordinates
				:returns: area
			"""
			w = 0.0
			n = len(self.coords)
			for i in range(n):
				j = (i + 1) % n
				w += (self.coords[j][0] + self.coords[i][0]) * \
					 (self.coords[j][1] - self.coords[i][1])
			return abs(w) /2.0

Az osztály definíciója a **class** alapszóval kezdődik. Az osztály neve
(**Polygon**) után a zárójelek között annak az osztálynak a neve jelenik meg,
melyből az aktuális osztályt származtatjuk (örölődés). Az osztály két
metódust (osztály tagfüggvényt) tartalmaz. A tagfüggvények első paramétere a
**self**, melyen keresztül az objektum példány tagváltozóit és tagfüggvényeit
érhetjük el.
Az **__init__** egy speciális 
függvény, melyet a Python környezet automatikusan meghív, amikor egy újabb 
példányt hozunk létre az osztályból (konstruktornak nevezik más OOP 
környezetekben). A tagfüggvény megőrzi a paramétert az objektum 
tagváltozójában. Az **area** függvényben csak annyi változás történt, hogy a 
pontok koordinátáit a **self** változó segítségével érhetjük el és nem kell
a paraméterlistán átadni a pontok koordinátáit. A felhasználás során az
osztályból egy példányt kell előállítanunk.

.. code:: python

    p0 = Polygon([[1, 1], [3, 1], [2, 2]])
    p1 = Polygon([[634110.62 , 232422.09 ],
        [634108.23, 232365.96],
        [634066.13, 232378.12],
        [634062.95, 232457.58],
        [634111.68, 232454.93],
        [634110.62, 232422.09]])
    print(p0.area())
    print(p1.area())

A **Polygon(...)** szolgál az objektum példány létrehozására.

Folyt. köv...
