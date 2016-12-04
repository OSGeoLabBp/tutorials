Esettanulmány 2
===============
Összeállította Bánhidi Dávid

Bevezetés
---------

Szögekkel kapcsolatos számításokra készítünk saját algoritmusokat, melyeket parancsként saját néven definiálunk majd osztályba gyűjtünk.


Fokból radiánt
--------------

Elsőként kezdjük egy egyszerű program megírásával, amely az általunk fok-perc-másodperc formában megadott szögértéket radiánban adja vissza. Ilyen függvényre azért van szükségünk, mert a Python trigonometriai függvényei csak radiánban adott szögeggel használhatók. Ha munkánkat az előzőekhez hasonlóan közvetlenül a Python konzolba írnánk, akkor minden alkalommal amikor fel szeretnénk használni számításunkhoz, kézzel be kellene írni. Ennél hatékonyabban járunk el, ha olyan kódsort készítünk, amelyet más programok írása közben meghívhatunk. Ehhez definiáljunk egy új függvényt, melyet egy fájlba írunk be.

.. code:: python

    import math
    
    def dms2rad(dms):
        """
            dms to radian
            input ddd-mm-ss
            return value in radian
        """
        items = dms.split('-')
        return math.radians(float(items[0])+float(items[1])/60.0+float(items[2])/3600.0)

Elsőként meghívjuk a math csomagot (a számítás során szükségünk lesz rá), majd definiáljuk a függvényünket, melynek neve dms2rad lesz, ezen a néven lehet majd meghívni. Emellett a név után zárójelben (vesszővel elválasztva) megadhatjuk, hogy hány paraméter tartozik a függvényhez és hogy azok milyen névvel kerüljenek tárolásra, mint változók. Majd rövid kommentben összefoglaljuk, hogy mire alkalmas a függvény, mik a bemenő és eredményként kapott értékei. Végezetül a számítást végző rész következik, ahol először "feldaraboljuk" a dms nevű változóban tárolt stringet (pl. '12-45-23'), majd egy lépésben másodperc és radián értékké alakítjuk.

Ha elmentjük a *dms2rad.py* fájlba és kipróbáljuk a frissen készített kódunkat, mondjuk a 123-34-45 értékkel (A Python konzolba írjuk be:

.. code:: python

    from dms2rad import *
    dms2rad('123-34-45')
    
Ezután megkapjuk a szöget radiánban. De mi van, ha azt írjuk be, hogy -22-13-45? És ha csak annyit, hogy 23-04? Mindkét alkalommal gondba ütközünk, hiszen a split függvény 3-nál több vagy kevesebb elemre bontja szét a dms változót, így nem megfelelő eredményt adba vissza, még ha hibamentesen le is fut a kód. Nézzünk egy javítás erre a problémára:

.. code:: python

    import math

    def dms2rad(dms):
        """
            dms to radian
            input ddd-mm-ss
            return value in radian
        """
        items = dms.split('-')
        while len(items) < 3:
            items.append('0') 
        return math.radians(float(items[0])+float(items[1])/60.0+float(items[2])/3600.0)

Láthatjuk, hogy beépítésre került egy ellenőrző vizsgálat, egy while ciklus segítségével addig pótoljuk ki 0 értékekkel az items változót, amíg az nem lesz 3 elemű. Ezzel kezeltük a túl rövid input paraméter hibáját. 

.. note:: Szorgalmi feladat

Hasonló vizsgálattal kezeljük a túl hosszú input paraméter problémáját, és írjunk ki hibaüzenetet. Illetve oldjuk meg a negatív előjel meglétének problémáját! Esetleg tegyünk kisérletet a nem megfelelő formátumban vagy nem megfelelő karaktereket (pl betűket is) tartalmazó bemeneti adat kezelésére is.


Ellenőrzés
----------

Beépíthetünk a python fájlunk végére ellenőrzést, mellyel a kód módosítása után gyorsan tesztelhetjük a működést.
Ehhez a következőket írjuk be az eddig meglévő kódunk végére:

.. code:: python
    
    if __name__== "__main__":
        print (dms2rad('12'))
        print (dms2rad('12-34'))
        print (dms2rad('12-34-56'))

Az *__name__* speciális Python változó (a dupla aláhúzással kezdődő és végződő nevek a Python környezet által használt speciális jelenetéssel bír), mely a futó kód indító fájljának nevét tartalmazza, ha az aktuális fájllal indítottuk a futtatást, akkor az "__main__" a tartalma. Azaz ha valamelyik Python fájlba importáljuk a dms2rad.py fájlt, akkor a feltételes blokkban lévő rész nem fog lefutni. Mivel már tudjuk kezelni a különböző módon megadott bemeneti paramétereket így mindre végezhetünk ellenőrzést, ahogy azt fent láthatjuk. 

Radiánból fokot
---------------

Készítsük el a visszafelé átváltást, tehát radiánból fok-perc-másodpercbe történő alakítást is.

.. code:: python

    import math
    
    def rad2dms(rad):
        """
            radian to dms
            input rad
            return value in dms
        """
        secs = round(rad * 180.0 / math.pi * 3600.0)
        mi,sec = divmod(secs, 60)
        deg,mi = divmod(mi, 60)
        deg = int(deg)
        return "%d-%02d-%02d" % (deg, mi, sec)

Hasonlóan az előzőhöz, itt legyen rad2dms a függvény neve. Számítás során kerekítés (round) és osztásmaradék (divmod) segítségével kapjuk meg az egyes köztes értékeket, majd a végén formázott szövegként írjuk vissza a számítás eredményét. Ezt a függvényt a dms2rad.py fájlba vigyük be.

Végül egészítsük ki az ellenőrző részt oda-visszaváltással:

.. code:: python

    if __name__== "__main__":
        print (rad2dms(dms2rad('12-23-34')))


Osztály létrehozása
-------------------

Ha az általunk írt sok 100 vagy 1000 soros kódban bizonyos rövidebb-hosszabb műveleteket jellemzően többször hajtunk végre, akkor célszerű lehet azon folyamatokra egy saját függvényt létrehozásni. Így növeljük a hatékonyságot, emellett átláthatóbb, igényesebb és újrahasznosítható kódot készíthetünk.

Tovább gondolva ezt a logikát, mi lenne, ha az így készített függvényeket valamilyen logika szerint csoportosítanánk? Itt érdemes megjegyezni, hogy a Python meglévő függvényei valójában jól rendszerezett, rövid algoritmusok tárháza, mely szabadon bővíthető és alakítható. (Utóbbival vigyázni kell, mert ha túl általános nevet adunk a függvényeinknek, akkor könnyen felülírhatunk egy általunk talán nem ismert, de beépített példányt, ami kellemetlenséget okozhat, ha "from modul import *" alakot használunk.) Az osztályok segítségével nem csak a program kódot csoportosíthajuk, hanem az azok által kezelt adatokat is. Az osztályok segítségével könyebben újrahasznosítható programkódot hozhatunk létre. Hozzunk létre egy ilyet (ezt is a dms2rad.py fájlba írhatjuk):

.. code:: python

    class Angle(object):
        """
            class to handle angles
        """
        def __init__(self,val = 0):
            self.setval(val)
        
        def setval(self,val = 0):
            if isinstance(val, str):
                self.val = dms2rad(val)
            else:
                self.val = val
                
        def __str__(self):
            return rad2dms(self.val)

Ne aggódjunk, ha ebből most nem értünk semmit! A lényeg számunkra az, hogy az eddigi szögszámításokkal kapcsolatos függvényeinket egy osztályból hívjuk meg, melynek neve Angle. Nézzünk erre is egy ellenőrzést:

.. code:: python

    if __name__ == "__main__":
        a = Angle('123-31-16')
        print(a)

Az "a" változó a szög osztáy egy példánya lesz, melynek megadjuk a kezdőértékét. A print eredménye fok-perc-másodpercben jelenik meg.

Nézzük meg kicsit részletesebben a kódot. A *class* alapszó egy új blokk kezdetét jelzi, mely egy Python osztály definíciója. Az osztály neve után (Angle) zárójelben a szülő osztály neve szerepel, az *object* a Python alaposztálya. Erről később az öröklődés kapcsán lesz szó. Az osztályon belül tagfüggvények (metódusok) definíciója szerepel. Ezek abban térnek el a korábbi függvény definícióktól, hogy a paramételistájuk a *self* változóval kezdőddik. A *self* változóval az aktuális osztály példányát érhetjük el. Az osztályunkat úgy készítettük el, hogy radiánban vagy fok-perc-másodpercben adott szögeket is tudjon fogadni. Az osztályhoz tartozó metódusokat (tagfüggvényeket) és a változókat a *self.* előtaggal érhetjük el. Az *__init__* egy spciális függvénye az osztálynak, mely minden újabb példány létrehozása esetén lefut automatikusan. Például az *a = Angle('123-31-16')* utasítás hatására létrejön egy új példány az *Angle* osztályból és az osztály *__init__* metódusát meghívja és a *val* paraméter értéke '123-31-16' lesz. Az objektum orientált programozás terminológiájában az ilyen tagfüggvényt konstruktornak nevezik.

A konstruktorunk a *setval* metódust hívja meg, mely először megvizsgálja, hogy a *val* paraméter string típusú-e. Ebben az esetben a fok-perc-másodpercet radiánba átszámító függvényünket hívjuk meg és a *self.val* nevű tagváltozóba helyezi el az értéket, ha nem szövegláncot tartalmaz a *val* paraméter, akkor azt feltételezzük, hogy a szög értékét radiánban tartalmazza és közvetlenül eltároljuk. Vigyázat a *val* és a *self.val* két külön változó, a sima *val* a függvény paramétere, mely az *__init__* függvényből kilépve már nem érhető el, a *self.val* az osztály tagváltozója, mely késöbb is elérhető az osztály példányán keresztül vagy a tagfüggvényekben.

Az *__str__* szintén egy speciális metódus, melyet a Python hívja meg, amikor egy *Angle* osztály példányát kiiratunk a *print* függvénnyel. Ezért jelenik meg a szög fok-perc-másodpercben a tesztelő kódunk lefutása után.
