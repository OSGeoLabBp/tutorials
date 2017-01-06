SAR install on rasberry pi (rasbian/jessie)
===========================================

.. code:: bash

    sudo apt-get update
    sudo apt-get upgrade

Install libudev-dev and libusb 1.0.18
-------------------------------------

.. code:: bash

    sudo apt-get install libudev-dev

Install libusb 1.0.18 from source
---------------------------------

.. code:: bash

    wget  http://downloads.sourceforge.net/libusb/libusb-1.0.18.tar.bz2
	tar xvjf libusb-1.0.18.tar.bz2
    cd libusb-1.0.18
    ./configure
    make 
    sudo make install

Install OpenGL
--------------

.. code:: bash

    sudo apt-get install xcompmgr libgl1-mesa-dri
    sudo apt-get install mesa-utils
    sudo apt-get install mesa-common-dev libgl1-mesa-dev libglu1-mesa-dev
    sudo apt-get install zlib1g-dev
    
Install VRui-3.1-004 
--------------------

.. code:: bash

    wget http://idav.ucdavis.edu/~okreylos/ResDev/Vrui/Vrui-3.1-004.tar.gz
    tar xfz Vrui-3.1-004.tar.gz
    cd Vrui-3.1-004
    make
    make install

Install Kinect-2.8-002
----------------------

.. code:: bash

    wget http://idav.ucdavis.edu/...
    tar xfz Kinect-2.8.tar.gz
    cd Kinect-2.8-002
    make

Install SARndbox-1.6
--------------------

.. code:: bash

    wget http://idav.ucdavis.edu/~okreylos/ResDev/SARndbox/SARndbox-1.6.tar.gz
    tar xfz SARndbox-1.6.tar.gz
    cd SARndbox-1.6
    make

