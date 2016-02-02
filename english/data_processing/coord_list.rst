Coordinate list processing with Unix text file utilities
========================================================

*Keywords*: text file processing, pipe, shell programing

*Data file*: lidat.txt (x, y, z)

Tasks to solve

*   At the beginning of data aquavision the sensor was not perfect, let's skip
    the first 100 lines

.. code:: bash

    tail -n +101 lidar.txt

*   Skip points above 1000 meter

.. code:: bash

    tail -n +101 lidar.txt | grep ",1[0-9]\{3\}\.[0-9]\+$"

or

.. code:: bash

    tail -n +101 lidar.txt | egrep ",1[0-9]{3}\.[0-9]+$"

*   Add a serial number to rows

.. code:: bash

    tail -n +101 lidar.txt | egrep -n ",1[0-9]{3}\.[0-9]+$"

*   Replace colon (:) after the serial number to coma (,)

.. code:: bash

    tail -n +101 lidar.txt | egrep -n ",1[0-9]{3}\.[0-9]+$" | sed "s/:/,/g" * > output_file

*   Add actual date to the end of file

.. code:: bash

    echo `date` >> output_file

or

.. code:: bash

    cat <<EOF >> output_file
    `date`
    EOF

or

.. code:: bash

    date >> output_file


All operations in two lines

.. code:: bash

    tail -n +101 lidar.txt | egrep -n ",1[0-9]{3}\.[0-9]+$" | sed "s/:/,/g" > lidar1.txt
    date >> lidar1.txt


All operations in one line

.. code:: bash

    (tail -n +101 lidar.txt | egrep -n ",1[0-9]{3}\.[0-9]+$" | sed "s/:/,/g" > lidar1.txt; echo `date`) > lidar1.txt


All operations in a shell script (coo.sh)

.. code:: bash

    #! /bin/bash
    tail -n +101 $1 | egrep -n ",1[0-9]{3}\.[0-9]+$" | sed "s/:/,/g"
    echo `date`

Run the script

.. code:: bash

    bash coo.sh lidar.txt > lidar1.txt

or

.. code:: bash

    . coo.sh lidar.txt > lidar1.tx

or

.. code:: bash

    chmod +x coo.sh lidar.txt > lidar1.tx
    ./coo.sh lidar.txt > lidar1.tx


*    Let's replace the second and third column

.. code:: bash

    cut -d "," -f1 lidar1.txt > c1.txt
    cut -d "," -f2 lidar1.txt > c2.txt
    cut -d "," -f3 lidar1.txt > c3.txt
    cut -d "," -f4 lidar1.txt > c4.txt;
    paste -d, c1.txt c3.txt c2.txt c4.txt > lidar2.txt

or

.. code:: bash

    gawk -F "," '{ print $1, $3, $2, $4 }' lidar1.txt > lidar2.txt

Let's rewrite our shell script to handle several input files and add the
column change, too.

.. code:: bash

    #! /bin/bash
    if [ $# -eq 0 ] ;then
        echo "usage $0 file(s)"
        exit 1
    fi
    for f in $@; do
        tail -n +101 $f | egrep -n ",1[0-9]{3}\.[0-9]+$" | sed "s/:/,/g" | gawk -F "," '{ print $1, $3, $2, $4 }'
        echo `date`
    done

.. note:: *Development tipps*:

    Select point in a rectangular area
