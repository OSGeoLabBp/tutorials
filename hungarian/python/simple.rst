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

Apéldához tartozó Python kódot a *gcd.py* fájlban találja a *code* 
alkönyvtárban.

Egész számok átváltása római számmá
-----------------------------------

A következő példában a római és arab számokra közötti átváltást oldjuk meg.
Itt arra törekszünk, hogy a lehető legkevesebb feltételes utasítssal oldjuk meg
a feladatot. Először az arabszámok rómaivá alakításával foglalkozzunk.
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
először váltsuk át a speciális két betűbőlálló részeket, ahol az első betű
számértéke kisebb mint az őt követő (pl. XC, CM, stb.). A római számoknál
nem létezik helyiérték így nek kell az elején vagya végén kezdeni az átváltást.
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
Ezek után a key értékeket a megadott sorrendben mg kell keresnünk az
átalakítandó római számban és az arab értékeiket összegezni egy változóban.
Ehhez 

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

