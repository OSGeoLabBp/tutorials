Hasznos modulok
===============

Ebben a leírásban néhány hasznos modult ismertetünk, a teljesség igénye nélkül.
A QGIS modulok gyűjtőhelyén jelenleg 443 modul találhatói, melyeket a QGIS
felhasználók készítettek és töltöttek fel a http://plugins.qgis.org oldalra.
Ezek közül választottam néhányat. De először a kezdőknek egy kis segítség a
modulok telepítésével kapcsolatban.

Modulok telepítése
------------------

A QGIS menüből a Modulok/Modulok kezelése és telepítése... menüponttal
kezdhetjük újabb modul telepítését, bekapcsolását illetve eltávolítását.

Egy modulnak három állapota lehet *nem telepített*, *telepített*, *aktív*.
A telepített modulokat tehetjük aktívvá, ekkor a QGIS betölti a modul kódját
és a modul felhasználói felülete megjelenik (ikon, menüpont, panel).

Egy másik szempont szerint belső ás külső modulokat különböztethetünk meg. 
A belső modulokat a QGIS fejlesztők tartják karban, azok a QGIS telepítésével
együtt kerülnek a gépünkre és nem tudjuk eltávolítani őket. A külső modulokat
a QGIS felhasználók készítik ezeket egyesével telepíthetjük és eltávolíthatjuk.
A külső modulokhoz csak kívételes esetben van magyar felhasználói felület,
általában angol üzenetekkel találkozhatunk.

A modulok között csak az aktuális QGIS verzióban használható modulok jelennek 
meg, ezek közül is azok, melyek a fejlesztő szerint stabilan működnek. A
kísérleti modulok megjelenítését a beállítások fülön kapcsolhatjuk be.
Itt a hivatalos QGIS modul tárház mellett továbbiakat is hozzáadhatunk (pl.
az Oslandia cég üzemeltett saját modul tárolót).

.. figure:: images/hasznos_modulok2.png
		:align: center

Új modul telepítéséhez válasszuk az **Mind** vagy a **Nem telepített** fület.
Célszerű a felső keresés mezőbe begépelni legalább részben a modul nevét, egy
rövidebb listában kelljen keresgélnünk.
A listából egy modulra kattintva a jobb oldalon rövid angol leírás 
illetve linkek jelennek meg. A felhasználók értékelését (csillagok) és a
letöltések számát is láthatjuk. A modul telepítés gomb megnyomásával települ
a gépünkre a modul. A telepített modul előtt egy jelölő négyzet jelenik, 
mellyek aktívvá tehetjük a modult

.. figure:: images/hasznos_modulok3.png
		:align: center

Ezután néhány modul ismertetése következik.

mapswipe
--------

Akinek rendszeresen űrfelvételeket, ortofotókat kell összehasonlítania, nagyon
hasznos lehet ez a modul. Vízszintesen vagy függőlegesen mozgathatunk egy 
vonalat a felső réteg eltkarásához vagy megjelenítéséhez.

A modul telepítése után a modulok menüből illetve eszközsorból érhető el a 
modul. Először a felső ortofotó/űrfelvétel legyen az aktív réteg és nyomjuk be a
modul ikonját az eszközsorban vagy a menübőé válasszuk ki. Az aktív réteg 
láthatóságát kikapcsolja a modul. Kattintsunk a térképre és nyomva tartott 
egér gombbal kezdjük belra-jobbra vagy le-fel húzni az egeret. Az egér gomb 
elengedése után újra kattintva módosíthatjuk a húzás irányát.

Nem csak rétegekre, hanem réteg csoportokra is lehet alkalmazni. Az alábbi
képen két WMS réteg esetét mutatja.

.. figure:: images/hasznos_modulok1.png
		:align: center

StreetView
----------


