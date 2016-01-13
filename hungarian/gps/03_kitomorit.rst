Compact rinex fájlok kitömörítése windows alatt
===============================================
*szerző: Takács Bence (takacs.bence@epito.bme.hu), BME Általános- és Felsőgeodézia Tanszék. utolsó módosítás: 2016. január 13.*

Korábban arról írtunk, hogyan lehet egy permanens állomás nyers mérési adatait `letölteni <https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/gps/01_gps_adatok_letoltese.rst>`_.
Rövid írásunk végén mutattunk egy shell scriptet, amelynek segítségével linux környezetben parancssorból letölthetünk és kitömöríthetünk mérési és navigációs állományokat. Ebben a rövid tanulmányban a compact rinex állományok windows operációs rendszer alatt, parancssorból történő kitömörítését mutatjuk be.

A kitömörítéshez szükséges programok windows operációs rendszer alá a következő `címről <http://terras.gsi.go.jp/ja/crx2rnx/RNXCMP_4.0.6_Windows_bcc.zip>`_ tölthetők le. Kitömörítés után célszerű a batch fájlokat és futtatható programokat tartalmazó könyvtárat hozzáadni a windows PATH rendszerváltozójához, így a compact rinex fájlok kitömörítése bármilyen könyvtárban elvégezhető. 

Célszerű a Z tömörítésű állományokat először kitömöríteni. Erre is kínálnak lehetőséget a fenti címről letöltött programok, de nekem jobban bevállt a `gzip <http://www.gzip.org/>`_ tömörítő program használata. Persze ezt is telepíteni kell és az elérési útvonalra (PATH) rátenni. Szóval parancssorból::

  gzip -d bute1520.15d.Z

A compact rinex mérési fájl pedig a következő paranccsal tömöríthető ki::

  CRZ2RNX bute1520.15d

A compact rinex mérési fájl ezután már törölhető::

  del bute1520.15d

A navigációs állományokat elegendő a gzip programmal kitömöríteni::

  gzip -d brdc1520.15n.Z
  gzip -d brdc1520.15g.Z

A kitömörítés lépéseit is hozzátehetjük a `python <https://github.com/OSGeoLabBp/tutorials/blob/master/hungarian/gps/02_gps_adatok_letoltese_python.rst>`_ szkriptünkhöz::

  import os
  cmd = 'gzip -df ' + station + doy + '0.' + year2 + 'd.Z'
  os.system(cmd)
  cmd = 'CRZ2RNX ' + station + doy + '0.' + year2 + 'd'
  os.system(cmd)
  
Egyben a python szkript, ami veszi a tegnapi nap dátumát és letölti a BME permanens állomásának mérési adatait, navigációs állományokat, majd mindezeket kitömöríti::

  #!/usr/bin/python
  # -*- coding: UTF-8 -*-
  """ download and uncompress GPS data from IGS station
  
  """
  #get date
  from datetime import date, timedelta
  yesterday = date.today() - timedelta(1)
  doy = yesterday.strftime('%j')
  year = yesterday.strftime('%Y')
  year2 = yesterday.strftime('%y')
  
  #download z compressed compact rinex observation file
  station='bute'
  ftp_server='ftp://igs.bkg.bund.de/EUREF/obs/'
  url =  ftp_server + year + '/' + doy + '/' + station + doy + '0.' + year2 + 'd.Z'
  import wget
  wget.download(url)
  
  #uncompress observation file
  import os
  cmd = 'gzip -df ' + station + doy + '0.' + year2 + 'd.Z'
  os.system(cmd)
  cmd = 'CRZ2RNX ' + station + doy + '0.' + year2 + 'd'
  os.system(cmd)
  cmd = 'del ' + station + doy + '0.' + year2 + 'd'
  os.system(cmd)
  
  #get and uncompress GPS and GLONASS navigation files
  station='brdc'
  ftp_server='ftp://igs.bkg.bund.de/EUREF/BRDC/'
  url =  ftp_server + year + '/' + doy + '/' + station + doy + '0.' + year2 + 'n.Z'
  wget.download(url)
  cmd = 'gzip -df ' + station + doy + '0.' + year2 + 'n.Z'
  os.system(cmd)
  url =  ftp_server + year + '/' + doy + '/' + station + doy + '0.' + year2 + 'g.Z'
  wget.download(url)
  cmd = 'gzip -df ' + station + doy + '0.' + year2 + 'g.Z'
  os.system(cmd)



