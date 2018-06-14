Bevezetés a QGIS szerver használatába
=====================================

Telepítés
---------

Ubuntu 16.04
~~~~~~~~~~~~

Előzőleg az *apache2*, *libapache2-mod-fcgid*, *qgis* és a *python-qgis* csomagokat telepíteni kell.

.. code:: bash

	sudo apt-get install qgis-server

A szerver indító programja a */usr/lib/cgi-bin/qgis_mapserv.fcgi* fájlba
kerül. Rögtön ellenőrizzük a telepítést a szerver indításával a parancssorból.

.. code:: bash

	/usr/lib/cgi-bin/qgis_mapserv.fcgi

Erre a következő üzenetet kapjuk:

.. code::

	Warning 1: Unable to find driver ECW to unload from GDAL_SKIP environment variable.
	Warning 1: Unable to find driver ECW to unload from GDAL_SKIP environment variable.
	Warning 1: Unable to find driver JP2ECW to unload from GDAL_SKIP environment variable.
	Initializing server modules from  "/usr/lib/lib/qgis/server" 

	"Checking /usr/lib/lib/qgis/server for native services modules"
	QFSFileEngine::open: No file name specified
	Content-Length: 54
	Content-Type: text/xml; charset=utf-8
	Server:  Qgis FCGI server - QGis version 3.0.3-Girona
	Status:  500

	<ServerException>Project file error</ServerException>

Ellenőrizzük a web szerver konfigurációt, a böngésző programba írjuk be a
következő URL-t:

.. code:: 

	http://localhost/cgi-bin/qgis_mapserv.fgci

Erre a következő *XML* dokumentumnak kell megjelennie:

.. code:: xml

	<ServiceExceptionReport version="1.3.0">
		<ServiceException code="Service configuration error">Service unknown or unsupported</ServiceException>
	</ServiceExceptionReport>

OSGeo Live
~~~~~~~~~~

Nem kell semmit sem telepíteni a QGIS Server készen áll a munkára.

Windows 10
~~~~~~~~~~

TBD OSGeo4W telepítés

QGIS projekt létrehozása
------------------------

Töltsük le a felhasznált shape fájlokat a http://www.agt.bme.hu/ftp/foss/mo.zip 
címről a bejelentkezési (home) könyvtárunkba (a későbbiekben erre a /home/user
névvel hivatkozunk, a user helyére a saját felhasználó nevét kell írnia).
Hozzunk létre egy új könyvtárat és tömörítsük ki a fájlokat.

.. code:: bash

	mkdir mo
	cd mo
	unzip ../mo.zip

Hozzuk létre a http://www.agt.bme.hu/gis/qgis/qgis_tutor_2.0.pdf oktatóanyagban
részletezett módon egy új QGIS projektet és mentsük el a */home/user/mo* 
könyvtárba *mo.qgs* névvel.

QGIS projekt publikálása
------------------------

TBD
