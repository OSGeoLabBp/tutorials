Permanens GPS állomás adatainak letöltése IGS ftp szerverről
============================================================
*szerző: Takács Bence (takacs.bence@epito.bme.hu), BME Általános- és Felsőgeodézia Tanszék.*

Példaként töltsük le a BME permamenens állomásának (BUTE) tegnap (2015. június 1-én) rögzített adatait.

**1. módszer:** böngészőből

* a böngészőbe írja be az adatokat tároló ftp szerver címét: ftp://igs.bkg.bund.de
* ezen belül navigáljon a megfelelő alkönyvtára, pl. /EUREF/obs/2015/152/, persze tudni kell, hogy 2015-ben június 1. az év 152. napja
* keresse meg és kattintson a letölteni a kívánt állomás méréseit tartalmazó állományra, esetünkben: bute1520.15d.Z

A módszer kivállóan működik egy-egy állomány letöltése esetén. Több állomány, esetleg automatizált letöltésére nem elegáns módszer.

**2. módszer:** ugyanez parancssorból. Az alábbi példákat linux operációs rendszeren készítettük. Egy terminal ablakba a következőket írja be::

	ftp
	ftp> open igs.bkg.bund.de
	Name (igs.bkg.bund.de:bence): anonymous
	Password: email@cimed.hu
	ftp> cd EUREF/obs/2015/152/
	ftp> get bute1520.15d.Z
	ftp> bye

Ez tulajdonképpen teljesen ugyanaz, mint a böngészőből történő letöltés, azzal a különbséggel, hogy a böngészőt kihagytuk.

**3. módszer:** shell scriptből. A shell script tartalma::

	#!/bin/sh
	ftp -in igs.bkg.bund.de <<ENDSCRIPT
	user anonymous email@cimed.hu
	cd EUREF/obs/2015/152/
	get bute1520.15d.Z
	bye
	ENDSCRIPT

**4. módszer:** shell scriptből, de a tegnapi nap dátumát automatikusan a számítógép dátumából vezessük le!::

	#!/bin/sh
	doy=$(date -d yesterday +"%j")
	year=$(date -d yesterday +"%Y")
	year2=$(date -d yesterday +"%y")
	ftp -in igs.bkg.bund.de <<ENDSCRIPT
	user anonymous email@cimed.hu
	cd EUREF/obs/$year/$doy/
	get bute$doy"0."$year2"d.Z"
	bye
	ENDSCRIPT

**5. módszer:** ftp program helyett wget használata. A terminal ablakba írja be::

	wget ftp://igs.bkg.bund.de/EUREF/obs/2015/152/bute1520.15d.Z

A wget előnye, hogy http protokollon keresztül, bejelentkezési adatok megadása nélkül is lehetővé teszi állományok parancssorból történő letöltését.
A dátum értelemszerűen lekérhető a 4. pontban említett módon. A script tartalma::

	#!/bin/sh
	doy=$(date -d yesterday +"%j")
	year=$(date -d yesterday +"%Y")
	year2=$(date -d yesterday +"%y")
	wget ftp://igs.bkg.bund.de/EUREF/obs/$year/$doy/bute${doy}0.${year2}d.Z

GPS és GLONASS navigációs állományok letöltése hasonlóan::

	#!/bin/sh
	doy=$(date -d yesterday +"%j")
	year=$(date -d yesterday +"%Y")
	year2=$(date -d yesterday +"%y")
	wget ftp://igs.bkg.bund.de/EUREF/obs/$year/$doy/bute${doy}0.${year2}d.Z
	wget ftp://igs.bkg.bund.de/EUREF/BRDC/$year/$doy/brdc${doy}0.${year2}g.Z
	wget ftp://igs.bkg.bund.de/EUREF/BRDC/$year/$doy/brdc${doy}0.${year2}n.Z

Compact rinex állományok kitömörítése
=====================================
A letöltött állományokat általában a unix/linux rendszerek Z tömörítő programjával, és az ú.n. compact rinex formátumban tömörítik. A kitömörítéshez kész programok, szkriptek állnak rendelkezésre. Letölthetők pl. az `oldalról <http://terras.gsi.go.jp/ja/crx2rnx.html>`_. A számítógépnek, operációs rendszernek megfelelő állományt töltsük le, tömörítsük ki! A programokat tartalmazó könyvtárat célszerű hozzáadni a *PATH* környzeti változóhoz. Linux alatt pl.::

	tar -xvzf RNXCMP_4.0.6_Linux_x86_32bit.tar.gz
	cd RNXCMP_4.0.6_Linux_x86_32bit/bin
	PATH="RNXCMP_4.0.6_Linux_x86_32bit:$PATH"
    
A szkriptek csh burokhoz készültek. Az én linuxomon (Ubuntu) a *csh*-t manuálisan kellett telepíteni::

	sudo apt-get install csh
    
Ezután a GNSS állományok kitömörítése egy csh burokból a következőképpen történik (parancsablakból természetesen)::

	CRZ2RNX bute1520.15d.Z
	CRZ2RNX bute1520.15n.Z
	CRZ2RNX bute1520.15g.Z

