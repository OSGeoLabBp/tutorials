Compact rinex fájlok kitömörítése windows alatt
===============================================
*szerző: Takács Bence (takacs.bence@epito.bme.hu), BME Általános- és Felsőgeodézia Tanszék. utolsó módosítás: 2015. június 10.*

Korábban arról írtunk, hogyan lehet egy permanens állomás nyers mérési adatait letölteni: https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/gps/gps_adatok_letoltese.rst.
Rövid írásunk végén mutattunk egy shell scriptet, amelynek segítségével linux környezetben parancssorból letölthetünk és kitömöríthetünk mérési és navigációs állományokat. Ebben a rövid tanulmányban a compact rinex állományok windows operációs rendszer alatt, parancssorból történő kitömörítését mutatjuk be.

A kitömörítéshez szükséges programok windows operációs rendszer alá a következő címről tölthetők le: http://terras.gsi.go.jp/ja/crx2rnx/RNXCMP_4.0.6_Windows_bcc.zip. Kitömörítés után célszerű a batch fájlokat és futtatható programokat tartalmazó könyvtárat hozzáadni a windows PATH rendszerváltozójához, így a compact rinex fájlok kitömörítése bármilyen könyvtárban elvégezhető. 

Célszerű a Z tömörítésű állományokat először kitömöríteni. Erre is kínálnak lehetőséget a fenti címről letöltött programok, de nekem jobban bevállt a gzip tömörítő program használata. Persze ezt is telepíteni kell és az elérési útvonalra (PATH) rátenni. Szóval parancssorból::

  gzip -d bute0060.16d.Z

A compact rinex mérési fájl pedig a következő paranccsal tömöríthető ki::

  CRZ2RNX bute0060.16d

A compact rinex mérési fájl ezután már törölhető:

  del bute0060.16d

A navigációs állományokat elegendő a gzip programmal kitömöríteni::

  gzip -d brdc0060.16n.Z
  gzip -d brdc0060.16g.Z
