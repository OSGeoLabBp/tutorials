SAR install on rasberry pi (rasbian/jessie) or Ubuntu 16.04
===========================================================

.. code:: bash

    sudo apt-get update
    sudo apt-get upgrade

Install libudev-dev
-------------------

.. code:: bash

    sudo apt-get install libudev-dev

Install devel libries
---------------------

.. code:: bash

    sudo apt-get install libjpeg-dev
    sudo apt-get install libpng-dev

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

Install VRui-4.2-006
--------------------

.. code:: bash

    wget http://idav.ucdavis.edu/~okreylos/ResDev/Vrui/Vrui-4.2-006.tar.gz
    tar xfz Vrui-4.2-006.tar.gz
    cd Vrui-4.2-006
    make
    sudo make install

Check make output if jpeg support is enabled before continue.

Install Kinect-3.2
------------------

.. code:: bash

    wget http://idav.ucdavis.edu/~okreylos/ResDev/Kinect/Kinect-3.2.tar.gz
    tar xfz Kinect-3.2.tar.gz
    cd Kinect-3.2
    make
    sudo make install

Install SARndbox-2.3
--------------------

.. code:: bash

    wget http://idav.ucdavis.edu/~okreylos/ResDev/SARndbox/SARndbox-2.3.tar.gz
    tar xfz SARndbox-2.3.tar.gz
    cd SARndbox-2.3
    make

