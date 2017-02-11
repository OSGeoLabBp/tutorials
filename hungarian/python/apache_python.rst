Apache Python modul használata
==============================

Ubuntu
------

Apache2 installálása

.. code:: bash

    sudo apt-get install apache2

mod_python installálása

.. code::

    sudo apt-get install libapache2-mod-python

Apache2 konfiguráció módosítása

Az */etc/apache2* könyvtárban az *apache2.conf* fájl végére tegyük be a következő sorokat:

.. code:: 

    # python
    <Directory /var/www/html>
        AddHandler mod_python .py
        PythonHandler mod_python.publisher
        PythonDebug On
    </Directory>

Ezzel az web szerver dokumentumok könyvtárában lévő *.py* fájlokat a python 
modullal fogja értelmezni.

Készítsünk egy kis teszt fájlt a */var/www/html* könyvtárba *test.py* névvel.

.. code:: python

    def index(req):
        return "Hello World"

Indítsuk újra az apache servert.

.. code:: bash

    sudo service apache2 restart

A böngészőbe írjuk be a *localhost/test.py* URL-t, a böngészőben a 
**Hello World** szövegnek kell megjelennie.

A HTML és Python kódot PHP-szerűen is egy fájlban kezelhetjük, ehhez az
apach2.conf konfigurációba a következő sorokat kell írnunk-

.. code::

    <Directory /var/www/html>
        AddHandler mod_python .psp
        PythonHandler mod_python.psp
        PythonDebug On
    </Directory>

Próbáljuk ki a következő Python fájlal (*test.psp*).

.. code:: html

    <html>
    <body>
    <h1><% req.write("Hello!") %></h1>
    </body>
    </html>

Források:

#. https://bhou.wordpress.com/2011/11/28/how-to-install-and-configure-mod_python-in-apache-2-server/
#. http://modpython.org/live/current/doc-html/installation.html
#. https://www.howtoforge.com/embedding-python-in-apache2-with-mod_python-debian-etch

Apache Python CGI használat
===========================

Ubuntu
------

Apache2 installálása, ha előzőleg nem történt meg

.. code:: bash

    sudo apt-get install apache2

CGI modul engedélyezése

.. code:: bash

    sudo a2enmod cgi

Apache2 újraindítása.

.. code:: bash

    sudo service apache2 restart

Az Apache2 alapértelmezett cgi-bin könyvtára a */usr/lib/cgi-bin*,
ezt az apache2.conf-ban ellenőrizhetjük.
A könyvtárban helyezzük el a következő Python szkriptet *pytest* névvel.

.. code:: python

    #!/usr/bin/env python
    print "Content-type: text/html\n\n"
    print "Hello CGI\n"

Módosítsuk a fájl attribútumait, hogy végrehajtható legyen.

.. code:: bash

    sudo chmod 755 /usr/lib/cgi-bin/pytest

A böngészőben írja be a *localhost/cgi-bin/testpy* URL-t. A *Hello CGI* 
üzenetnek kell megjelennie.

Hivatkozások:

#. https://bdhacker.wordpress.com/2011/05/21/running-your-first-cgi-program-with-apache2/
#. https://bdhacker.wordpress.com/2011/05/21/running-your-first-cgi-program-with-apache2/

PostgreSQL telepítése
=====================

Linux
-----

.. code:: bash

	sudo apt-get install postgresql postgresql-client-common postgis pgadmin3

PostgreSQL felhasználó és adatbázis létrehozása, PostGIS engedélyezése.

.. code:: bash

	sudo su - postgres
	psql -c "create user név"
	psql -c "create database db_név"
	psql -c "alter database db_név owner to név"
	psql -d db_név -c "create extension postgis"

psycopg2 és SQLAlchemy telepítése
=================================

Linux
-----

.. code:: bash

	# python 2.x
	sudo apt-get install python-psycopg2
	pip install sqlalchemy
	# python 3.x
	sudo apt-get install python3-psycopg2
	pip3 install sqlalchemy

Adatbázis tábla létrehozása, feltöltése
=======================================

.. code:: SQL

	CREATE TABLE pdata (
		id varchar(20) NOT NULL,
		easting double precision,
		northing double precision,
		elev double precision,
		d timestamp NOT NULL,
		PRIMARY KEY(id, d));

.. code:: SQL

	INSERT INTO pdata VALUES ('1', 100.012, 200.016, NULL, '2017-02-10 9:30');
	INSERT INTO pdata VALUES ('1', 100.018, 200.012, NULL, '2017-02-11 12:25');
	INSERT INTO pdata VALUES ('2', 105.621, 300.165, NULL, '2017-02-10 9:31');
	INSERT INTO pdata VALUES ('2', 105.617, 300.162, NULL, '2017-02-11 12:26');

psycopg2 használata
===================

.. code:: python

	import psycopg2
	conn = psycopg2.connect("dbname=siki user=siki")
	cur = conn.cursor()
	cur.execute("SELECT * FROM pdata")
	for row in cur:
		print row
	cur.close()
	conn.close()

SQLAlchemy használata
=====================

.. code:: python

	from sqlalchemy import create_engine
	from sqlalchemy import MetaData, Column, Table, PrimaryKeyConstraint
	from sqlalchemy import String, DateTime, Float
	from sqlalchemy.sql import select
	import datetime

	metadata = Metadata()
	engine = create_engine('postgresql:///siki', echo=True)
	conn = engine.connect()
	pdata = Table('pdata', metadata,
		Column('id', String(20)),
		Column('easting', Float),
		Column('northing', Float),
		Column('elev', Float),
		Column('d', DateTime),
		PrimaryKeyConstraint('id', 'd'))
	metadata.create_all(engine)
	s = select([pdata])
	result = conn.execute(s)

	for row in result:
		print row

ORM (object relation model) használata:

.. code:: python

