:Author: Zoltan Siki
:License: Creative Commons Attribution-ShareAlike 3.0 Unported  (CC BY-SA 3.0)

*******************************************************************************
Segédlet az OSGeo Live DVD magyar fordításához
*******************************************************************************

Kezdő lépések
~~~~~~~~~~~~~

Az OSGeo Live DVD szöveges anyagait a GitHub portál tartalmazza. A fordítás
kezdésekor készítettem egy másolatot a saját repozitorimba, mivel nincs jogom
közvetlenül az eredeti repozitoriba írni. Ez a 
https://github.com/zsiki/OSGeoLive-doc linken érhető el. Ehhez a tárhelyhez
kaphatnak a fordításban részvevők írási jogot is. Ahhoz, hogy a fordításba
bekapcsolódj a következőket kell tenni:

* regisztálj a GitHub oldalon (sign up)
* küldd el nekem a GitHub nevedet (a jelszó nem kell!),
  és hozzáadlak a közreműködőkhöz
* telepítsd a **git** klienst a gépieden

Ubuntu, Debian::

  $ sudo apt-get install git

RedHat, Fedora::

  $ sudo yum install git

Windows:

  Töltsd le a Windows telepítőt a http://git-scm.com/download/win címről.

Készíts egy másolatot a GitHub repozitorimról a saját gépeden (kb. 450 MB)::

  $ git clone https://github.com/zsiki/OSGeoLive-doc

A fenti parancs az aktuális könyvtárban készít egy OSGeoLive-doc könyvtárat,
ennek **hu** alkönyvtárába lesznek a magyar fordítások. A következőkben Linux
környezetet feltételezünk, az ott használható parancsokat adjuk meg.

.. note::
   A szövegeket UTF-8 kódlappal kell szerkeszteni, olyan szövegszerkesztő
   programot kell választani mely alkalmas erre. Linux-on általában ez az
   alapértelmezett kódlap. 

Fordítás kezdése
~~~~~~~~~~~~~~~~

A munka megkezdése előtt a következőket célszerű egyszer beállítani a *git* 
konfigurációban::

  git config --global user.name "GitHub_felhasználó_név"
  git config --global user.email "your_email@example.com"
  git config --global core.editor vi

A **vi** helyére a kedvenc szövgszerkesztődet írhatod.
A fenti beállítások a gépen lévő összes projektre érvényesek lesznek, ha egy-egy
projektre eltérő beállításokat akarsz, akkor lépj be a projekt könyvtárába és a
**--global** kapcsoló nélkül add ki a parancsokat. 

A beállításokat le is ellenőrizheted az alábbi parancsokkal::

  git config --global user.name
  git config --global user.email
  git config --global core.editor

A munka kezdésekor mindig aktualizáld a helyi repozitoridat, lépj be a
helyi repozitory könyvtárába vagy annak valamelyik alkönyvtárába::

  cd OSGeoLive-doc
  git pull

Válassz ki egy fájlt az **en** könyvtárból vagy az **en/overview** vagy az
**en/quickstart** kkönyvtárból, amit még nem fordítottak le eddig.
Másold át a fájlt a megfelelő **hu** könyvtárba. Például::

  cd OSGeoLive-doc/hu/quickstart
  cp ../../en/quickstart/osm_quickstart.rst .

Küldj egy üzenetet a többi fordítónak, hogy te fordítod ezt a fájlt.
Ezután nyisd meg a választott szövegszerkesztő programmal a fájl. Például::

  vi osm_quickstart.rst

A fájl elején található Author direktívák után írd be magad mint fordító::

  :Translator: ide írd a neved

Ezután kezd el a fordítást.

.. note::
   Az rST formátumban az üres soroknak és a sorok beugratásának is jelentősége
   van. Először érdemes egy rST oktató anyagot elolvasni 
   (http://docutils.sourceforge.net/docs/user/rst/quickstart.html).

Nem kell egy menetben elvégezned a fordítást, sőt jobb, ha a GitHub repozitoriba
visszatöltés előtt mégegyszer átolvasod a munkádat.

Néhány tanács a fordításhoz

* ne használj magyarban szenvedő szerkezetet
* ne ragaszkodj a szószerinti fordításhoz, a tartalom legyen azonos
* a gyostalpaló (quickstart) dokumentációknál az adott szoftverben is
  csináld végig a gyakorlatokat a fálreértések elkerülése végett
* legalább még egyszer olvasd át a fordításodat, mielőtt feltöltöd a 
  GitHub-ra
* az elkészült fordításokat az átolvasás után minél hamarabb töltsd fel a
  GitHub-ra
* célszerű előbb az overview dokumentumot lefordítani és utána a quickstart-ot

A lefordított új fájlt először hozzá kell adnod a helyi repozitoridhoz
(feltételezzük, hogy a lefordított fájlt tartalmazó könyvtárban vagy és az
ossim_quickstart.rst fájlt fordítottad le), ezt
csak egyszer kell megcsinálni az új fájlokra::

  git add ossim_quickstart.rst

Készítsd elő a fájl a GitHub repozitoriba felküldéshez::

  git commit osm_quickstart.rst

Ez a parancs után a git konfigurációban beállított szövegszerkesztő program
jelenik meg, az első sorba be kell írnod, hogy mi volt a változás. Ezt az
alábbi formátumban tedd meg::

  HU: osm_quickstart initial translation

mennyiben más jellegű javítást történt, akkor azt írd le (de angolul),
például::

  HU: osm_quickstart review

A **git commit** parancs csak a helyi repozitoriban jelöli meg a fájlt, ezeket
egy további paranccsal kell feltölteni a GitHub repozitoriba::

  git push

A parancs kiadása után a GitHub felhasználói nevünket és a jelszavunkat is meg
kell adni. Ekkor kerülnek fel a **commit** paranccsal megjelölt fájlok a 
többiek által is látható repozitoriba a GitHub szerveren.

A **git** számos további parancsot tartalmaz, ezekről például a
https://git-scm.com/docs/gittutorial dokumentumban olvashatsz.

