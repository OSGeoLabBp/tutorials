Esettanulmány
=============

Bevezetés
---------

A prím számok kikeresésére szolgáló algoritmus példáján a hatékony algoritmus 
kialakítását és a Pythonic kód készítését mutatjuk be.

Első naiv algoritmus
--------------------

Prím szám az a természtes szám melynek két osztója van (önmaga és egy). A legkisebb
prím szám a kettő. Egy számról úgy dönthetjük el prím-e, hogy végig próbáljuk a kisebb
számokkal mennyi lesz az osztási maradékuk. El kell menni az oszthatóság vizsgálatával
*n-1*-ig ha *n* a vizsgált szám? A szám gyökénél nagyobb számokra nem érdemes vizsgálnunk
hiszen például a 24 esetén a négyes osztó megtalálása után nincs jelentősége, hogy
négyeshez tartozó osztópárt (6) is megtaláljuk. 
Ez Python-ban így nézhet ki:

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.0
    """

    import math
    import time

    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, 500001):   # find prims up to 50000
        prime = True
        for divider in range(2, int(math.sqrt(p))+1):
        if p % divider == 0:     # remainder of division is zero
            prime = False        # it is not a prime
        if prime:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

Az algoritmus hatékonyságát az algoritmusunk futási idejével mérjük.
A mai számítógépeken mindig több alkalmazás, szolgáltatás fut párhuzamosan, ezért az
egyszeri időmérés nem ad mindig átlagos eredményt, Célszerű többször futtatni az 
átlagos futási idő megtalálásához.

Első hatékonyságnövelés
-----------------------

A fenti algoritmus 105 esetén 11-ig tart az osztók vizsgálata, azonban a 3-as osztó
megtalálása után felesleges tovább folytatni a belső ciklust, már eldőlt nem prím
számról van szó. Módosítsuk az algoritmus, hogy az első osztó megtalálása után 
a belső ciklusból lépjen ki (break utasítás).

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.1
    """
    
    import math
    import time
    
    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, 500001):   # find prims up to 50000
        prime = True
        for divider in range(2, int(math.sqrt(p))+1):
            if p % divider == 0: # remainder of division is zero
                prime = False    # it is not a prime
                break            # divider found no need to continue
        if prime:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))
    
Python 2.7 verzióval futtatva a gépemen az első változat több mint 20 másodpercig fut.
A második változat már négy másodpercnél kevesebbet. Az egymásba ágyazott ciklusok
esetén a belső ciklus futásának a lerövidítése nagy hatékonyság növekedéssel jár.

.. note::

    Érdekes, hogy Python 3 verzióban (3.5) futtatás esetén a program futási ideje növekszik.
    
Tegyük Pythonikussá a kódot
---------------------------

A bevezetőben említettük, hogy nem csak a hatékonyság, hanem a Pythonikus (Pythonic) kód
kialakítása is a célunk. A Python nyelvben a ciklushoz is rendelhetünk egy **else** 
utasítást, mely akkor hajtódik végre, ha nem léptünk ki a ciklus futtatásából **break**
utsítással. Ennek felhasználásával rövidebbé tehetjük a kódunkat és ezzel talán
könnyebben olvashatóvá. Feleslegessé válik a prím logikai változó használata.
Emellett tegyük könnyebben felhasználhatóvá a kódunkat, hogy a parancssorban
adhassuk meg a prím keresés felső korlátját. Erre a **sys** standard modult használjuk,
a modul az **argv** listában a parancssorban megadott paramétereket szolgáltatja.

.. code:: python

    """
        naive algorith to find prime numbers
        version 1.2
    """
    
    import math
    import time
    import sys
    
    max_num = 101
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    prims = []                   # list of prims
    for p in range(2, max_num):  # find prims up to max_num
        for divider in range(2, int(math.sqrt(p))+1):
            if p % divider == 0: # remainder of division is zero
                break            # divider found no need to continue
        else:
            prims.append(p)      # store prime number
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))
    

Ezzel a módosítással a kódunk nem vált hatékonyabbá, de a kevesebb utasításból álló
kód előnyösebb.

Minden szám felbontható prím számok szorzatára. Így az oszthatóság vizsgálatot
elég az előzőleg megtalált prím számokra végrehajtani. Módosítsuk az algoritmusunkat.

.. code:: python

	"""
		naive algorith to find prime numbers
		version 1.3
	"""

	import math
	import time
	import sys

	max_num = 101
	if len(sys.argv) > 1:        # check command line parameter
		max_num = int(sys.argv[1]) + 1
	start_time = time.time()
	prims = []                   # list of prims
	for p in range(2, max_num):  # find prims up to max_num
		maxp = int(math.sqrt(p))+1
		for divider in prims:    # enough to check prims!
			if p % divider == 0: # remainder of division is zero
				break            # divider found no need to continue
			if maxp < divider:
				prims.append(p)
				break
		else:
			prims.append(p)      # store prime number
	print('ready')
	print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

Hatékonyabb algoritmus
----------------------

Az előzőekben az eredeti elképzelésünket megtartva módosítottuk a kódot a hatékonyság 
érdekében. Lehet, hogy az eredeti elképzelésünk átértékelésével juthatunk hatékonyabb 
megoldáshoz? Ez már Eraszthotenésznek is sikerült az eraszthotenészi szita 
kitalálásával. Ennek alapgondolata, hogy ne az egyes vizsgált számok osztásával 
keressük a prímeket, hanem állítsuk elő a természetes számok sorozatát és 
ebből távolítsuk el az egyes számok többszöröseit. Ez valahogy így nézhet ki:

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.0
    """
    
    import math
    import time
    import sys
    
    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = range(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        numbers[j+j::j] = [0 for k in numbers[j+j::j]] # use sieve
    
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))
    
A kódban a listaértelmezést (list comprehension) alkalmaztuk. Ez gyorsabb mint a lista
**for** típusú ciklussal előállítása. A

.. code:: python

    [0 for k in numbers[j+j::j]]

sor egy nullákat tartalmazó listát állít elő, melynek a hossza megfelel a *j* érték
többszöröseinek számának. Az értékadással a számok listájában nullázzuk a *j* érték
többszöröseit. Nem lehetett volna egyszerűen a következő értékadást írni?

.. code:: python

    numbers[j+j::j] = 0

Sajnos ez nem működik, egy lista részének nem adhatunk értékül egy skalárt, de a [0] 
sem működik az értékadás jobb oldalán, mert az is csak folytonos részére működne az
eredeti listának.

Ez a változat fél millióig a prím számokat 3 tized másodperc alatt állítja elő. Az első
algoritmusunkhoz képest százszoros gyorsulást értünk el.

.. note::

   A fenti kód Python 3 verzióban nem működik. Python 3-ban a **range** függvény nem egy
   listát ad vissza, hanem egy generátort, ezt a **list** függvénnyel át kell
   alakítanunk listává.

Lehet még gyorsítani?
---------------------

Elemezzük egy kicsit a kódunkat. A *j* ciklusváltozó a 2, 3, 4, ... értékeket veszi 
fel a futás során, így először 4-től nullázzuk az összes páros számot, majd 6-tól
minden harmadik számot, majd 8-tól minden negyediket. Álljunk meg itt egy pillanatra!
Minek nullázzuk a néggyel osztható számokat? Azokat már a kettővel oszthatóság miatt 
nulláztuk. Hasonló a helyzet például a kilenccel osztható számokkal, azokat már a 
hárommal oszthatóság miatt nulláztuk. Azaz nem kell minden *j*-re az elemek 
nullázását végrehajtani, erre csak akkor van szükség, ha *j*-ik elemet még nem
nulláztuk. Ez egy plusz feltétellel tehetjük meg, mellyel a kód hosszabb lesz, de
hatékonyabb.

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.1
    """
    
    import math
    import time
    import sys
    
    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = range(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = [0 for k in numbers[j+j::j]] # use sieve
    
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))
    
Ennek a módosításnak a hatékonyság növelő hatása fél millióig futtatva kevésbé
jelentkezik. Ennek az is az oka, hogy az algoritmusunk futási ideje maximális
prím szám növelésével nem lineárisan növekszik.

A lista értelmezés hatékonyabb módszer a listák előállítására mint a "sima" **for**
ciklus. Azonban az esetünkben az előállított lista minden eleme nulla. A lista
értelmezést arra használjuk, hogy a lista hosszát be tudjuk állítani.
Erre viszont létezik egy egyszerűbb (pythonikusabb) megoldás. Ha egy listát egy 
egész számmal szorzunk, akkor az eredmény a lista többszörözése. A

.. code:: python

   [0] * 5

utasítás egy öt hosszúságú nullákat tartalmazó listát eredményez.
Nézzük meg, hogy egy ilyen átalakítás növeli-e a hatékonyságot!

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.2
    """
    
    import math
    import time
    import sys
    
    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = range(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = [0] * len(numbers[j+j::j]) # use sieve
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))
 
Ezzel a módosítással öt millióig a prím számok kikeresése már kevesebb mint egy 
másodpercbe telik a gépemen.

A numpy könyvtár még egy kicsit gyorsíthat
------------------------------------------

A numpy Python modul számos matemetikai probléma megoldásába kész megoldásokat 
nyújt a programozóknak. Mi a numpy tömb kezelését és több tömb elemre 
érték adást használjuk fel.

.. code:: python

    """
        Sieve of Erasthotenes prim algorithm
        version 2.2
    """
    
    import math
    import time
    import sys
    import numpy as np
    
    max_num = 1001
    if len(sys.argv) > 1:        # check command line parameter
        max_num = int(sys.argv[1]) + 1
    start_time = time.time()
    numbers = np.arange(max_num)     # list of natural numbers to check
    for j in range(2, int(math.sqrt(max_num))):
        if numbers[j]:
            numbers[j+j::j] = 0 # use sieve
    prims = sorted(list(set(numbers) - set([0, 1]))) # remove zeros from list
    print('ready')
    print('%d prims in %f seconds' % (len(prims), time.time() - start_time))

A numpy modul importlásán kívül csak két sor módosult. A számok előálltása 
során egy numpy tömböt hozunk létre az *arange* függvénnyel. A gyorsítást a
második módosítás jelenti, az elemek nullzásához nem kell előállítanunk 
annyi nulla elemből álló listát, ahány elemet nullázni szeretnénk.
Ezzel további 10% körüli gyorsulást érhetünk el, persze itt ebbe nem számítottukbe a numpy modul betöltésének idejét.

Az egyes algoritmusokat a 100000-nél és 1000000-nál kisebb prím számok kikeresére
futtattuk. Az alábbi táblázat tartalmazza a futási időket:

+--------+----------------+----------------+----------------+
| Verzió | Futási idő [s] | Futási idő [s] | Futási idő [s] |
|        |    100000      |   1000000      |  10000000      |
+--------+----------------+----------------+----------------+
|   1.0  |       1.90     |      60        |       -        |
+--------+----------------+----------------+----------------+
|   1.1  |       0.45     |      10        |     326        |
+--------+----------------+----------------+----------------+
|   1.2  |       0.44     |      11        |     333        |
+--------+----------------+----------------+----------------+
|   1.3  |       0.21     |       2.62     |      50        |
+--------+----------------+----------------+----------------+
|   2.0  |       0.07     |       0.58     |       6.41     |
+--------+----------------+----------------+----------------+
|   2.1  |       0.04     |       0.32     |       2.99     |
+--------+----------------+----------------+----------------+
|   2.2  |       0.02     |       0.19     |       1.73     |
+--------+----------------+----------------+----------------+
|   2.3  |       0.03     |       0.17     |       1.61     |
+--------+----------------+----------------+----------------+



Itt kifogytam az ötletekből. Van ötlete a gyorsításra? Ossza meg velünk!
