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

#https://bhou.wordpress.com/2011/11/28/how-to-install-and-configure-mod_python-in-apache-2-server/
#http://modpython.org/live/current/doc-html/installation.html
#https://www.howtoforge.com/embedding-python-in-apache2-with-mod_python-debian-etch

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

#https://bdhacker.wordpress.com/2011/05/21/running-your-first-cgi-program-with-apache2/
#https://bdhacker.wordpress.com/2011/05/21/running-your-first-cgi-program-with-apache2/

