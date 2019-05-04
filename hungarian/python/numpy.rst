numpy modul
===========

A numpy a Python nyelv vektorok és mátrixok kezelésére specializált 
modulja. 

A Python nyelvben a vektorok és mátrixok kezelését a listák segítségével is 
megoldhatjuk, de az kevésbé hatékony (mivel eltérő Python adattípusok
lehetnek ugyanannak a listának az elemei). A numpy további előnye, hogy 
számos vektorokkal, mátrixokkal kapcsolatos műveletet készen tartalmaz.

Tömbök létrehozása
------------------

A numpy tömbökben az elemek csak azonos típusúak lehetnek, jellemzően
egész, lebegőpontos és logikai típusú elemeket használunk.
Numpy tömböket létrehozhatunk speciális numpy függvényekkel vagy listákból.

.. code:: python

	import numpy as np
	a = np.zeros(9).reshape(3, 3)	# 3 x 3 nullákat tartalmazó mátrix
	a = np.zeros((3, 3))			# ugyanaz mint az előző sor
	a.dtype							# a mátrix elemeinek típusa
	b = np.random.rand(6)			# 6 elemű véletlen vektor
	i = np.eye(4)					# 4 x 4 egységmátrix
	# mátrix létrehozása listából adott elemtípussal
	c = np.array([[1, 2, 3], [2, 4, 6]], dtype=np.int32)
	c.shape							# tömböknek tulajdonságai is vannak
	c.size
	d = np.arange(10)				# 0..9 elemekből álló vektor
									# np.array(range(10)) is lehetne
	e = np.arange(2, 11, 2)			# páros számok 10-ig
	f = np.arange(0.1, 1, 0.1)		# nem csak egész értékeke lehetnek
	f = np.linspace(0.1, 0.9, 9)	# ugyanaz mint az előző

Tömbök indexelése
-----------------

A numpy tömbök indexelése a listához hasonlóan történik. Index tartományok
megadásával is operálhatunk.

.. code:: python

	t1 = np.arange(80).reshape(10,8)
	print(t1[0,0])					# indexelés szögletes zárójellel
	print(t1[0][0])					# ugyanaz mint az előző
	print(t1[2])					# harmadik sor
	print(t1[:,1])					# második oszlop
	print(t1[::2])					# minden második sor
	print(t1[t1 % 3 == 0])			# tömb elemek szűrése, hárommal oszhatók

Műveletek tömbökkel
-------------------

A numpy az Octave-tól (Matlap) eltérően az alapműveleteket elemenként végzi el,
azaz két tömb szorzata elemenkénti szorzatot jelent.

.. code:: python

	a1 = np.full((3, 4), 8)
	a2 = np.arange(12).reshape(3, 4)
	print(a1 - a2)
	print(a1 * a2)					# elemenkénti szorzat!
	print(a2**2)					# minden elem négyzete!
	print(np.sqrt(a2))

A numpy a mátrix szorzásra a dot függvényt biztosítja. a linalg modulban
több hasznos függvényt találhatunk, mintpéldául *inv, pinv, svd, eig, det,
solve*.

.. code:: python

	b1 = np.arange(12).reshape(4, 3)
	print(b1.transpose().dot(b1))	# transzponált szorzata a mátrix-szal
	print(b1.T.dot(b1)				# azonos az előzővel
	bb1= np.linalg.inv(b1.T.dot(b1))

Gyakorlati példák
-----------------

Polynom illesztés
~~~~~~~~~~~~~~~~~

Illesszünk regressziós polinomot (legkiseb négyzetek módszerével) megadott
pontokra. A pontok koordinátái egy fájban (pontok.txt) találhatók, soronként
egy pont adatai.

.. code:: txt

	1.1 0.4
	2.6 1.9
	4.2 3.0
	7.0 3.1
	8.2 2.4
	9.6 1.2

.. code:: python

	import numpy as np
	from math import sqrt
	pnts = np.genfromtxt('pontok.txt', delimiter=' ')	# pontok egy tömbbe
	c = np.polyfit(pnts[:,0], pnts[:,1], 2)				# parabola illesztés
	v = np.polyval(c, pnts[:,0]) - pnts[:,1]			# maradék ellentmondások
	rms = sqrt(np.sum(v**2) / pnts.shape[0])			# négyzetes átlagos hiba

Ábrázoljuk az eredményeket grafikusan a matplotlib modul segítségével.

.. code:: python

	import matplotlib.pyplot as plt
	plt.plot(pnts[:,0], pnts[:,1], 'bx')				# adott pontok
	plt.scatter(pnts[:,0], pnts[:,1], marker='x')		# azonos az előzővel
	x = np.linspace(np.min(pnts[:,0]), np.max(pnts[:,0]), 100)
	plt.plot(x, np.polyval(c, x))						# függvény görbe
	plt.show()

Magassági hálózat kiegyenlítés
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Készítsünk egy szintezési hálózat kiegyenlítésére alkalmas programot.
Két bemenő állománnyal dolgozunk. Az egyikben a pontok 
magassága, a másikban a szintetési vonalak adatai (kezdő sorszám, záró sorszám,
magasságkülönbség, hossz) találhatók. Program szabad magassági hálózat 
kiegyenlítést számít.

.. code:: text

	104.234
	103.487
	102.958
	101.345

.. code:: text

	1 2 -0.749 1.1
	1 3 -1.274 1.8
	1 4 -2.890 1.4
	2 3 -0.530 1.5
	2 4 -2.141 1.9
	3 4 -1.614 0.9

.. code:: python

	import numpy as np

	elev = np.genfromtxt('elev.txt', delimiter=' ')
	obs = np.genfromtxt('obs.txt', delimiter=' ')

	mkm = 0.7                       # 0.7 mm/km
	n = elev.size                   # ismeretlenek száma
	m = obs.shape[0]                # egyenletek száma
	A = np.zeros((m, n))            # alakmátrix
	P = np.zeros((m, m))            # súlymátrix
	P[[np.arange(m), np.arange(m)]] = 1 / (obs[:, -1] * mkm)**2
	A[[np.arange(m), obs[:,0].astype(int)]] = -1
	A[[np.arange(m), obs[:,1].astype(int)]] = 1
	l = obs[:,-2] - A.dot(elev)     # tisztatagok
	Ninv = np.linalg.pinv(A.T.dot(P).dot(A))
	x = Ninv.dot(A.T).dot(P).dot(l) # magasság változások
	v = A.dot(x) - l                # javítások
	X = elev + x                    # kiegyenlített magasságok
