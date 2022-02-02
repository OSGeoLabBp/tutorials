Pythonic kód készítés
=====================

Ebben a kis oktatóanyagban egyszerű matematikai problémák Python megoldását
mutatjuk be.

Legnagyobb közös osztó
----------------------

Találjuk meg két szám legnagyobb közös osztóját. Egy naív megoldás lehet
a két számot az összes lehetséges számmal elosztani és az osztási maradékot 
vizsgálni. A két szám közül kisebbnél nagyobb közös osztó nem lehet. A
hatékonyság érdekében a vizsgálatot a nagyobb számoktól lefelé végezzük.
Az alábbi függvény egy lehetséges megoldása a problémának:

.. code:: python


	def gcd_naiv(a, b):
		""" find greatest common divisor of a and b """
		for i in range(min(a, b), 1, -1):
			if a % i == 0 and b % i == 0:
				return i
		return 1

A példában a *range* függvényt használtuk a lehetséges osztók előállítására,
csökkenő sorrendben. Például a *range(5, 1, -1)* a következő sorozatot
állítja elő: *[5, 4, 3, 2]*. A *%* operátor két egész érték osztási maradékát
számítja. Az első olyan szám megtalálásakor, melynek a két bejövő értékkel 
az osztási maradéka nulla megtaláltuk a megoldást (mivel csökkenő sorrendben
haladunk). Amennyiben aciklusunk végéig nem találunk mindkét számhoz osztót,
akkor 1 értéket ad vissza a függvényünk.

Próbáljuk ki a fenti kódot, feltételezve, hogy a függvény kódját a *gcd_naiv.py*
fájlba írtuk be. 

.. code:: python

	from gcd_naiv import gcd_naiv
	gcd_naiv(32, 80)

Az eredmény 16 lesz.

Miért neveztük naívnak a kódot? Nagy számok esetén lassú ez a megoldás. Már
Euklidesz talált egy hatékonyabb rekurzív algoritmust:

.. code:: python

	gcd(a, 0) = a
	gcd(a, b) = gcd(b, a % b)

A fenti rekurzív algoritmus Python megvalósítása a következő lehet:

.. code:: python

	def gcd_rec(a, b):
		""" find greatest common divisor of a and b Euclid's algorithm"""
		if b == 0:
			return a
		return gcd_rec(b, a % b)

Rekurzióról akkor beszélünk, ha egy függvény közvetlenül vagy közvetve
önmagát hívja. A rekurzió általában rövid és könnyen áttekinhető kódot
eredményez, de sok memóriát használhat.

Nézzünk meg egy nem rekurzív megoldást:

.. code:: python

	def gcd(a, b)
		""" find greatest common divisor of a and b, non-recursive Euclid's algorith"""
		while b:
			a, b = b, a % b
		return a

A fenti kódot tartalmazza a Python fractions modulja is. Ez is meglehetősen 
rövid kód. Két részletre térnénk ki itt. a *while b:* sor azt jelenti,hogy a
ciklusunkat addig hajtsuk végre, amíg b értéke nulla nem lesz (egyenértékű a
*while b != 0* sorral). Ez abból következik, hogy az egész számok logikai 
értékként is lehet használni. A nulla a hamis logikai értéket jelenti, minden
más érték az igaz logikai értéket. A cikluson belüli sor egyidőben két 
változó értékét változtatja meg, például Pythonban két változó értékét 
egysoros utasításssal megvalósíthatjuk: *x,y = y, x*.

Próbálja ki a fenti kódot a fractions modulból:

.. code:: python

	from fractions import gcd
	gcd(32, 80)

A példához tartozó Python kódot a *gcd.py* fájlban találja a *code* 
alkönyvtárban.

Egész számok átváltása római számmá
-----------------------------------

A következő példában a római és arab számokra közötti átváltást oldjuk meg.
Itt arra törekszünk, hogy a lehető legkevesebb feltételes utasítással oldjuk meg
a feladatot. Először az arab számok rómaivá alakításával foglalkozzunk.
A feladat megoldásához egy segédlistát hozunk létre, mely egyrészt az
egy jegyű (egy-három között ismételhető) római számok értékét illetve a
speciális két betűből állókat tartalmazza (amikor az első szám kisebb mint az
utánakövetkező pl. IV, CD, stb.) valamint  nekik megfelelő arab számokat, az 
arabszámok csökkenő sorrendjében.

.. code:: python

	roman = ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
	         (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
	         (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))

Ezután már "csak" a fenti listán kell végigmenni és amíg az átváltandó szám
értéke nagyobb mint a *roman* listában az egész szám az eredmény szöveglánchoz
hozzá kell adni a római számot és az eredeti számot az értékével csökkenteni.
A megoldást egy Python függvénybe helyezzük el:

.. code:: python

	def toroman(n):
		""" convert integer to its roman equivalent e.g. 456 -> CDLVI """
		result = ""
		for item in roman:
			while n >= item[0]:
				result += item[1]
				n -= item[0]
		return result

Ennyi az egész.

.. note::

	Vigyázat a fenti megoldás 4000 vagyannál nagyobb számokra nem működik.
	Ezen számok ábrázolása nem lehetséges római számokkal.

Próbáljuk meg megoldani az átváltást visszafelé is. Itt a logikánk az lesz, hogy
először váltsuk át a speciális két betűből álló részeket, ahol az első betű
számértéke kisebb mint az őt követő (pl. XC, CM, stb.). A római számoknál
nem létezik helyiérték így nem kell az elején vagy a végén kezdeni az átváltást.
Ismét egy segéd listát és egy segéd szótárat hozunk létre az algoritmus
egyszerűsítésére:

.. code:: python

	arabic = {'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400,
			  'CM': 900, 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100,
			  'D': 500, 'M': 1000}
	keys = ('IV', 'IX', 'XL', 'XC', 'CD', 'CM', 'I', 'V', 'X', 'L', 'C', 'D', 'M')

Vegyük észre, hogy a *keys* listában elől vannak a kétbetűből álló speciális 
esetek (a *keys* lista az *arabic* szótárból is előállítható lenne:
*list(arabic.keys())*, ha megfelelő a szótárban az elemek sorrendje).
Ezek után a key értékeket a megadott sorrendben meg kell keresnünk az
átalakítandó római számban és az arab értékeiket összegezni egy változóban.

.. code:: python

	def toint(s):
		""" Convert roman number to int """
		result = 0
		s = s.upper()
		for key in keys:
			while key in s:
				result += arabic[key]
				s = s.replace(key, "", 1)
		return result

A fenti függvényben a *replace* szövegláncokra alkalmazható függvényt egy 
előfordulás cseréjére használjuk, ezt jelenti a harmadik paraméterben az egyes.
A *replace* függvény az összes előfordulást lecseréli alapértelmezésben.

Vegyük észre, hogy az *arabic* szótárból a a *roman* lista is előállítható:
*roman = sorted(list(zip(arabic.values(), arabic.keys())))[::-1]*

A feladat megoldását a *roman.py* fájl tartalmazza a *code* alkönyvtárban.

Hurkok keresése egy irányítatlan gráfban
----------------------------------------

Egy gráf leírását az éleket tartalmazó fájllal adjuk meg. A gráfra kikötjük
hogy két csomópont között csak egy közvetlen kapcsolat lehet. Az éleket
a kezdő és vég csomópont azonosítóival írjuk le, emellett az él hosszát
és a végpontok magasságkülönbségét tároljuk.

.. code:: tet

    1 +-------+2            Élek listája
      |      /|        kezdő vég   táv   dm
      |     / |          1    2     1    0.51
      |    /  |          2    3     2   -0.19
      |   /   |          3    4     1    0.11
      |  /    |          4    1     2   -0.38
      | /     |          4    2     2.5  0.12
      |/      |
     4+-------+3

A hurkok keresését először a mélységben lépő algoritmussal valósítottuk meg.
Az alábbi kódot például arra használhatjuk, hogy egy szintezési hálózatban 
a körzárásokat ellenőrizzük.

A hurok keresést minden egyes élre végrehajtjuk. A kezdeti élet egyesével 
növeljük a csatlakozó élek közül (addp függvény). Egy hurok megtalálása 
esetén vizsgáljuk, hogy más élből indulva megtaláltuk-e már ezt. Két hurkot
a benne lévő csomópontok száma és a csomópontokból alkotott halmazok
összehasonlításával valósitjuk meg. Például a [1, 2, 4, 1] és a
[4, 2, 1, 4] hurkok hossza (4) azonos és a belőlük alkotott halmazok
{1, 2, 4} is azonosak.

Végül a hosszuk alapján rendezzük a hurkokat, összegezzük a hosszakat és
a magasságkülönbségeket és kiírjuk az eredményt.

.. code:: python

    #! /usr/bin/env python

    """
        Search for all loops in an undirected graph using deep first search
        and sum up distances and a values of edges in each loop.

        Usage: loops.py input_file

        ascii input file format for a line/edge (space separated):
        startp endp distance value
    """

    import sys

    def addp(edges, loop, indx):
        """ find and add a point to the loop
            :param edges: edges of graph
            :param loop: actual loop
            :param indx: edge indices

            :returns: extended loop and new indx as a tuple
        """
        for i in range(indx[-1], len(edges)):
            edge = edges[i]
            if edge[0] == loop[-1] and edge[1] != loop[-2] and edge[1] not in loop[1:]:
                # connection to start point
                loop.append(edge[1])
                indx[-1] = i
                indx.append(0)
                return loop, indx
            if edge[1] == loop[-1] and edge[0] != loop[-2] and edge[0] not in loop[1:]:
                # connection to end point
                loop.append(edge[0])
                indx[-1] = i
                indx.append(0)
                return loop, indx
        return loop, indx

    if len(sys.argv) < 2:
        print (f"Usage: {sys.argv[0]} input_file")
        sys.exit()
    else:
        fname = sys.argv[1]
    edges = []
    edges_dic = {}
    i = 0
    # loading input file
    with open(fname, "r") as f:
        for line in f:
            l = line.split()
            i += 1
            ll = tuple(l[:2])
            edges.append(ll)
            try:
                edges_dic[ll] = (float(l[2]), float(l[3]))
            except:
                print("Error in input file line: ", i)
                exit(-1)
     # find all unique loops
    loops = []
    for edge in edges:
        loop = [edge[0], edge[1]]
        indx = [0, 0]
        while True:
            n = len(loop)
            loop, indx = addp(edges, loop, indx)
            if loop[0] == loop[-1]:     # closed loop found
                n1 = len(loop)
                s1 = set(loop)
                for loop2 in loops:     # check same loop found?
                    if n1 == len(loop2) and s1 == set(loop2):
                        break
                else:
                    loops.append(loop[:])   # make a copy of list
                n = len(loop)           # force back step
            if len(loop) == n:
                # no new point or loop found step back
                loop.pop()
                indx.pop()
                indx[-1] += 1
                if len(loop) < 2:       # no more step back
                    break
    loops.sort(key=len)                 # sort loop by length
    n = 0
    m = len(loops[-1])                  # length of longest loop
    # sum up distances and values
    print("Value Distance Loop")
    for i, loop1 in enumerate(loops):
        n += 1
        # calculate sum distance and value
        sdist = 0
        sdm = 0
        last = loop1[0]                 # start point
        for node in loop1[1:]:
            indx = last,node
            if indx in edges_dic:       # forward direction
                sdist += edges_dic[indx][0]
                sdm += edges_dic[indx][1]
            else:                       # reverse direction
                indx = node,last
                sdist += edges_dic[indx][0]
                sdm -= edges_dic[indx][1]
            last = node
        print (f"{sdm:.3f} {sdist:8.1f} {loop1}")
    print(f"Number of loops: {n}, Max loop length: {m}")
