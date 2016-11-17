Esettanulmány 2
===============

Bevezetés
---------

Szögekkel kapcsolatos számításokra készítünk saját algoritmusokat, melyeket parancsként saját néven definiálunk majd osztályba gyűjtünk.


Fokból radiánt
--------------

Elsőként kezdjük egy egyszerű program megírásával, amely az általunk fok-perc-másodperc formában megadott szögértéket radiánban adja vissza. Ha munkánkat az előzőekhez hasonlóan egy tetszőleges .py fájlba írva mentekénk el, akkor minden alkalommal amikor fel szeretnénk használni számításunkhoz, külön meg kellene nyitnunk és kézzel beleírni/átírni a változót, hogy lefuttatása után megkaphassuk az eredményt. Ennél hatékonyabban járunk el, ha olyan kódsort készítünk, amelyet más programok írása közben meghívhatunk. Ehhez deffiniálnunk kell egy új függvényt.

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

Elsőként meghívjuk a math csomagot (a számítás során szükségünk lesz rá), majd deffiniáljuk a függvényünket, melynek neve dms2rad lesz, ezen a néven lehet majd meghívni. Emellett a név után zárójelben (vesszővel elválasztva) megadhatjuk, hogy hány paraméter tartozik a függvényhez és hogy azok milyen névvel kerüljenek tárolásra, mint változók. Majd rövid kommentben összefoglaljuk, hogy mire alkalmas a függvény, mik a bemenő és eredményként kapott értékei. Végezetül a számítást végző rész következik, ahol először "feldaraboljuk" a dms nevű változóban tárolt stringet, majd egy lépésben másodperc és radián értékké alakítjuk.

Ha elmentjük és kipróbáljuk a frissek készített kódunkat, mondjuk a 123-34-45 értékkel ( Shell-be írjuk be: dms2rad('123-34-45') majd ENTER ) akkor megkapjuk a szöget radiánban. De mivan ha azt írjuk be, hogy -22-13-45? És ha csak annyit, hogy 23-04? Mindkét alkalommal gondba ütközünk, hiszen a split függvény 3-nál több vagy kevesebb elemre bontja szét a dms változót, így nem megfelelő eredményt adba vissza, még ha hibamentesen le is fut a kód. Nézzünk egy javítás erre a problémára:

.. code:: python

    import math

    def dms2rad(dms):
        """
            dms to radian
            input ddd-mm-ss
            return value in radian
        """
        items = dms.split('-')
        while len(items)<3:
            items.append('0') 
        return math.radians(float(items[0])+float(items[1])/60.0+float(items[2])/3600.0)

Láthatjuk, hogy beépítésre került egy ellenőrző vizsgálat, egy while ciklus segítségével addig pótoljuk ki 0 értékekkel az items változót, amíg az nem lesz 3 elemű. Ezzel kezeltük a túl rövid kezdeti paraméter hibáját. 

Szorgalmi feladat
-----------------

Hasonló vizsgálattal kezeljük a túl hosszú kezdeti paraméter problémáját, és írjunk ki hibaüzenetet. Illetve oldjuk meg a negatív előjel meglétének problémáját! Esetleg tegyünk kisérletet a nem megfelelő formátumban vagy nem megfelelő karaktereket (pl betűket is) tartalmazó bemeneti adat kezelésére is.


Ellenőrzés
----------

Beépíthetünk automatikus ellenőrzést az algoritmusunk végére, amelynek kifejezetten az objektumorientált programozás (OOP) során van jelentőssége. Így tudjuk vizsgálni, hogy egy módosításnak köszönhetően megjelent hiba melyik függvényen belül okozott gondot, ezzel gyorsítva és akár automatizálva a hibakeresés folyamatát.

Ehhez a következőket írjuk be az eddig meglévő kódunk végére:

.. code:: python
    
    if __name__== "__main__":
        print (dms2rad('12'))
        print (dms2rad('12-34'))
        print (dms2rad('12-34-56'))

Mivel már tudjuk kezelni a különböző módon megadott bemeneti paramétereket így mindre végezhetünk ellenőrzést, ahogy azt fent láthatjuk. 

Radiánból fokot
---------------

Készítsük el a visszafelé, tehát radiánból fokba történő alakítást is.

.. code:: python

    import math
    
    def rad2dms(rad):
        """
            radian to dms
            input rad
            return value in dms
        """
        secs = round(rad*180.0/math.pi*3600.0)
        mi,sec = divmod(secs,60)
        deg,mi = divmod(mi,60)
        deg = int(deg)
        return "%d-%02d-%02d" % (deg,mi,sec)

Hasonlóan az előzőhöz, itt legyen rad2dms a függvény neve. Számítás során kerekítés (round) és osztásmaradék (divmod) segítségével kapjuk meg az egyes köztes értékeket, majd a végén formázott szövegként írjuk vissza a számítás eredményét.

Szintén végezhetünk ellenőrzést:

.. code:: python

    if __name__== "__main__":
        print (rad2dms(dms2rad('12-23-34')))


Osztályok létrehozása
---------------------

Ha az általunk írt sok 100 vagy 1000 soros kódsorban bizonyos rövidebb-hosszabb műveleteket jellemzően többször hajtunk végre, akkor célszerű lehet azon folyamatokra egy saját függvényt létrehozásni. Így növeljük a hatékonyságot, emellett átláthatóbb és igényesebb kódot készíthetünk.

Tovább gondolva ezt a logikát, mi lenne, ha az így készített függvényeket valamilyen logika szerint csoportosítanánk? Itt érdemes megjegyezni, hogy a Python meglévő függvényei valójában jól rendszerezett, rövid algoritmusok tárháza, mely szabadon bővíthető és alakítható. ( Utóbbival vigyázni kell, mert ha túl általános nevet adunk a függvényeinknek, akkor könnyen felülírhatunk egy általunk talán nem ismert, de beépített példányt, ami kellemetlen gondokat okozhat. ) A rendszerezés logikájára az osztályok (class-ok) szolgálnak. Hozzunk létre egy ilyet:

.. code:: python

    class Angle(object):
        """
            class to handle angles
        """
        def __init__(self,val=0):
            self.setval(val)
        
        def setval(self,val=0):
            if isinstance(val,str):
                self.val = dms2rad(val)
            else:
                self.val = val
                
        def __str__(self):
            return rad2dms(self.val)

Ne aggódjunk, ha ebből most nem értünk semmit! A lényeg számunkra az, hogy az eddigi szögszámításokkal kapcsolatos programocskákat összefoglaljuk egy osztályba, melynek neve Angle. Ha eképpen deffiniálunk egy változót, akkor pusztán az objektum típusának ismeretében el tudjuk dönteni, hogy az most egy fok-perc-másodperc érték vagy egy radián. Nézzünk erre is egy ellenőrzést:

.. code:: python

    if __name__ == "__main__":
        a = Angle('123-31-16')
        print(a)

Az "a" változót deffiniáljuk stringként, emellett megadjuk, hogy ennek osztálya Angle. 
