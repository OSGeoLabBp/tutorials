Generate report from a DXF file
===============================

*Keywords*
: text file processing, associative array

*Data file*
: test.dxf

*Program files*
: dxfinfo.awk

In this receipt a report is generated from a DXF file. The generated table
contains layer name and entity name pairs with the number of entities.
Entities section of the DXF file is scanned for code 0 (entity type) and
code 8 (layer name).
Associative array is used to simulate multidimensional array.

Sample data (test.dxf), start of the entities section:

.. code::

    SECTION
      2
    ENTITIES
      0
    LINE
      5
    3F
    330
    1F
    100
    AcDbEntity
      8
    0

gawk code:

.. code::

    #!/bin/gawk -f
    # 
    # statistics about entities and layers in a DXF file
    # Zoltan Siki siki.zoltan@epito.bme.hu
    # usage: dxfinfo.awk your_file.dxf
    #		or
    #        gawk -f dxfinfo.awk your_file.dxf > statistics.txt

    BEGIN { # initialize variables
        last = ""; entity = ""; layer = "";
    }
    /ENTITIES/,/ENDSEC/ { # process only the entities section
        if (last == "  0") {	# last row entity start code?
            entity = $0;
        } else if (last == "  8") {	# last row layer name code?	
            layer = $0;
            dxf[layer,entity]++;	# increment entity count for layer, entity combination
        }
        last = $0;	# remember last input row
    }
    END {	# print out result
        for (i in dxf) {	# for each layer,entity pairs
            split(i, w, SUBSEP);	# separate layer and entity in index into w array
            print w[1], w[2], dxf[i];	# print layer, entity anc count
        }
    }

The first comment line '#!/bin/gawk -f' is the shebang used by unix/linux 
shell scripts. If you set the execute (x) bit for the file, you can start it 
entering the script name at the commnd promp. For example:

.. code::

    chmod +x dxfinfo.awk   # do it only ones
    ./dxfinfo.awk test.dxf

The result is sent to the standard output in arbitrary order. We should send 
the result to sort to get a clearer output.

.. code::

    ./dxfinfo.awk test.dxf | sort

.. note:: *Development tipps:*

    Subentities are not handled correctly, e.g. VERTEX inside a POLYLINE or 
    ATTRIBUTE inside a block INSERT. Change code to handle subentities, too.
