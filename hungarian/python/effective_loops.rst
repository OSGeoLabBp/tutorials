Python ciklus szerkezetek összehasonlítása
==========================================

Ebben a kis anyagban arra mutatunk példákat, hogy milyen ciklus szerkezetek 
hatékonyabbak a Pythonban.


Természetes számok összege (code/fastest_loop.py)
-------------------------------------------------

Az első példában az egész számok összegét fogjuk képezni nullától n-1-ig.
Első lépésben egy **while** típusú ciklus készítsünk erre. A későbbi futási
időmérés érdekében függvényt készítünk az összeg képzésére

.. code:: python

    def while_loop(n=100_000_000):
        """ using pure while loop """
        i = 0
        s = 0
        while i < n:
            s += i
            i += 1
        return s

A fenti megoldásban mindent a kezünkben tartunk a ciklus változó (**i**)
növelését és az összeg képzését (**s**). A Pythonban írt kód sokkal lasabb
mint a C/C++ nyelven írt kód. A Python beépített függvényeit C nyelven 
írják, ezért célszerűbb beépített függvény (**range**) és **for** ciklus
segítségével megoldani a ciklusváltozó léptetését.

.. code:: python

    def for_loop(n=100_000_000):
        """ using for and range """
        s = 0
        for i in range(n):
            s += i
        return s

A **for** ciklus és a **range** függvény használatával kb. 30%-kal csökken
a ciklus futási ideje. A ciklus futási idejét leghatékonyabban úgy tudjuk
csökkenteni, ha nem használunk ciklust. A **sum** Python függvény segítségével
ciklus nélkül képezhetjük az összeget.

.. code:: python

    def sum_func(n=100_000_000):
        """ using built in sum function """
        return sum(range(n))

Ezzel csak C-ben írt függvényeket hívunk a Python kódból és a futási időt 
az első megoldás hatodára csökkenthetjük. Még ennél is gyorsabb megoldást
kaphatunk a **numpy** modul segítségével.

.. code:: python

    import numpy as np
    def numpy_sum(n=100_000_000):
        """ using numpy arange and sum """
        return np.sum(np.arange(n))

Így már huszadára csökkentettük az eredeti **while** ciklus futatási idejét.
Azonban még ne dőljünk hátra, jusson eszünkbe, hogy van egy egyszerű, zárt
képlet az összeg kiszámítására, mellyel a C-ben futó ciklusokat is 
kiválthatjuk.

.. code:: python

    def math_logic(n=100_000_000):
        """ using math formula """
        return n * (n + 1) // 2

Ez a megoldás összehasonlíthatatlanul gyorsabb mint az előzőek.

Futási idők:

.. code::

    while loop:    5.899067100001048
    for loop:      3.937892075000491
    sum function : 1.1208928319992992
    numpy sum    : 0.26107627999954275
    math logic   : 2.3229986254591495e-06

Műveletek egy vektor elemeivel (vector.py)
------------------------------------------

Ebben a példában egy lista minden elemét megszorozzuk egy számmal, amiből
egy újabb listát állítunk elő. A megoldás során egyre hatékonyabb kódot
készítünk.

Az első megoldás során **while** ciklust használunk és egyesével építjük fel 
az eredmény listát.

.. code:: python

    def while_loop(m=2.5, n=100_000_000):
        """ using pure while loop """
        i = 0
        l = []
        while i < n:
            l.append(m * i)
            i += 1
        return l

Ebben az esetben már csak kb. 10%-os gyorsítást érhetünk el a **for**
ciklussal és a **range** függvény használatával.

.. code:: python

    def for_loop(m=2.5, n=100_000_000):
        """ using for loop and range """
        l = []
        for i in range(n):
            l.append(m * i)
        return l

A listából listát létrehozó feladatok esetén a Python egy speciális
algoritmus szerkezetet a *lista feldolgozást* (list comprehesion) kínálja.
Ez hatékonyabb megoldást biztosít a hagyományos ciklusoknál. A kiinduló
megoldshoz képest 20-25% gyorsulást érhetünk el ezzel, amellett hogy a
kódunk jóval tömörebb lett.

.. code:: python

    def list_compr(m=2.5, n=100_000_000):
        """ list comprehension """
        return [m * i for i in range(n)]

A Python **map** függvényével a lista minden elemére ugyanazt a függvényt
alkalmazhatjuk amélkül, hogy ciklus szerkezetet használnánk. Ezzel már érdemi 
gyorsulást nem tudunk elérni. Itt még egy speciális megoldást, a helyben
definiált név nélküli függvényt (*lambda függvény*) használunk. Ez a 
megoldást a lista feldolgozással azonos sebességgel dolgozik.

.. code:: python

    def map_func(m=2.5, n=100_000_000):
        """ using built in map function """
        return map(lambda x: x * 2.5, range(n))

A **map_func** függvényünk nem listát, hanem egy *map* objektumot ad vissza.
Ezt a **list** függvénnyel konvertálhatjuk listává.

Végül ebben az esetben is nézzük meg a *numpy*-t használó megoldást.
Ebben az esetben érdemi gyorsítást a *numpy* sem biztosít az előző két
megoldáshoz képest.

.. code:: python

    def numpy_vec(m=2.5, n=100_000_000):
        """ using numpy vector """
        return np.dot(np.arange(n), m)

Ennek a függvénynek az eredménye egy *numpy* tömb, melyet szintén a 
**list** függvénnyel alakíthatunk át listává, ha szükséges.

Végül az egyes megoldások futási idejei:

.. code:: 

    while loop:         9.250859855001181
    for loop:           7.363860025998292
    list comprehension: 7.065938151998125
    map function:       7.016882312000234
    numpy vector:       7.006166957999085

