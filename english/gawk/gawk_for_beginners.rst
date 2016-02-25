gawk for beginners
==================

gawk (GNU awk) is a programable unix text utility. It is one of the most complex
of them. Several simple example will be introduced to teach you by examples.

gawk processes the input text file line by line. Each line is devided intos
fields using a set of field separators. The default field separators are *TAB* 
and *space*.  We can refere to a field in the actual line by $1 (first field),
$2 (second field), etc. $0 gives the whole actual input line.

There are some variables maintained by gawk. The most important ones are:

* *NF* number of fields in the actual input line
* *NR* row number in input file
* *FS* field separator(s)

The gawk program can be given in the command line if it is very short or we
can create a separate file for the program. The usual extension for gawk
program file is *.awk*.

gawk reads data from the input file or from the standard input and prints
output to the standard output.

The syntaxis of the gawk programs are very similiar to C programs. gawk can be 
a good start point to learn C.

Add row numbers to a text file
------------------------------

.. code:: gawk

    gawk '{ print NR, $0 }' /etc/passwd

The example above will print back the Linux password file with line numbers to
the standard output. The output of the gawk command can be redirected to 
the a file e.g.

.. code:: gawk

    gawk '{ print NR, $0 }' /etc/passwd > row_num_passwd

Remove columns from input file
------------------------------

.. code:: bash

   gawk -F : '{ print $1, $3, $5 }' /etc/passwd

The example above will print out the Linux user names, user ID and full name.
After the -F switch a custom field separator can be defined. The *cut* command
can be used to generate the same output.

.. code:: bash

    cut -d : -f 1,3,5 /etc/passwd

Reverse the field order of the input lines
------------------------------------------

.. code:: gawk

    { for (i = NF; i > 0; i--) { printf "%s:", $i; }
      print "\n";
    }

The *for* command is to count iterations. *i* is the loop variable and changed
from the number of fields (*NF*) down to *1*. We can refere to the *ith* field
by *$i*. *printf* is for formatted print, it won't print new line at the end.
*print "\n";* prints a new line character.

This case we create a separate file for the gawk program. Copy the program
above into a file called *reverse.awk*. Then use the following commad to run
this gawk program.

.. code:: bash

    gawk -F : -f reverse.awk /etc/passwd

Print only unique lines from the file
-------------------------------------

.. code:: gawk

    {
        if (prev != $0) {
            print $0;
        }
        prev = $0;
    }

The code above will work only for sorted files. Let's list the different 
login shells from the password file (the last field in the row).

.. code:: bash

    gawk -F : '{ print $NF; }' /etc/passwd | sort | gawk -f unique.awk

First the login shell fields are extracted, then the sort command is used to 
sort the file before using *unique.awk*.

Word counts in a file
---------------------

.. code:: gawk

    {
        for (i = 1; i <= NF; i++) {
            words[$i]++;
        }
    }

    END {
        for (w in words) {
            print words[w], w;
        }
    }

Copy the code above into *words.awk* file. The first part of the code (between
the curly brackets) is executed for each input line of the file and fills an 
array, the index of the array is the word, 
the value of the array element is the count for that world. The second part
of the program, after the *END* will be executed ones, after all input lines
were processed.

Let's list the first ten most frequent words from the gawk manual page.

.. code:: bash

    man gawk | gawk -f words.awk | sort -nr | head -10

Coordinate list from M5 electric fieldbook
------------------------------------------

M5 is the data file format for Trimble M3 total stations. It looks like this:

.. code:: text

    For M5|Adr 00017|TI      EL STAT                |                      |                      |                      |
    For M5|Adr 00018|PI1           !               2|                      |                      |Z           0.000 m   |
    For M5|Adr 00019|PI1           A               2|SD          7.674 m   |Hz         7.5439 DMS |V1        89.1413 DMS |
    For M5|Adr 00020|PI1           S               A|                      |                      |Z          -0.102 m   |
    For M5|Adr 00021|TI      PR                     |th          0.000 m   |PC         -0.030 m   |A           0.005 m   |
    For M5|Adr 00022|TI      POLAR                  |                      |                      |                      |
    For M5|Adr 00023|PI1                           B|SD         40.701 m   |Hz       259.0155 DMS |V1        89.4419 DMS |
    For M5|Adr 00024|PI1                           B|Y          60.043 m   |X         192.256 m   |Z           0.083 m   |
    For M5|Adr 00025|PI1                           C|SD         42.898 m   |Hz       191.1129 DMS |V1        89.4510 DMS |
    For M5|Adr 00026|PI1                           C|Y          91.674 m   |X         157.918 m   |Z           0.083 m   |
    For M5|Adr 00027|PI1                           D|SD         37.521 m   |Hz        74.1237 DMS |V1        89.4334 DMS |
    For M5|Adr 00028|PI1                           D|Y         136.105 m   |X         210.210 m   |Z           0.077 m   |
    For M5|Adr 00029|TI      DR                     |th          0.000 m   |PC          0.000 m   |A           0.035 m   |
    For M5|Adr 00030|TI      POLAR                  |                      |                      |                      |
    For M5|Adr 00031|PI1                         A11|SD          8.702 m   |Hz       356.0147 DMS |V1        89.1228 DMS |
    For M5|Adr 00032|PI1                         A11|Y          99.398 m   |X         208.680 m   |Z           0.018 m   |
    For M5|Adr 00033|PI1                         A12|SD          8.131 m   |Hz       359.1339 DMS |V1        89.0730 DMS |
    For M5|Adr 00034|PI1                         A12|Y          99.890 m   |X         208.130 m   |Z           0.022 m   |
    For M5|Adr 00035|PI1                         A13|SD          7.699 m   |Hz         9.2341 DMS |V1        89.0933 DMS |
    For M5|Adr 00036|PI1                         A13|Y         101.257 m   |X         207.595 m   |Z           0.011 m   |

.. code:: gawk

    BEGIN {
        FS = "[\|]";    # field separator
    }

    /\|Y / {            # y coordinate given in the input line
        y = x = z = 0;
        for (i = 1; i <= NF; i++) {         # check all fields
            if (match($i, /^PI1[ \t]+/)) {  # point id
                id = substr($i, 20);        # skip first 20  chars
                sub(/^ +/, "", id);         # remove leading spaces
            } else if (match($i, /^Y[ \t]+/)) { # y coordinate
                y = substr($i, 2);          # skip first character
                sub(/^ +/, "", y);          # remove leading spaces
                sub(/ m +$/, "", y);        # remove trailing spaces and dimension
            } else if (match($i, /^X[ \t]+/)) { # x coordinate
                x = substr($i, 2);          # skip first character
                sub(/^ +/, "", x);          # remove leading spaces
                sub(/ m +$/, "", x);        # remove trailing spaces and dimension
            } else if (match($i, /^Z[ \t]+/)) { # z coordinate
                z = substr($i, 2);          # skip first character
                sub(/^ +/, "", z);          # remove leading spaces
                sub(/ m +$/, "", z);        # remove trailing spaces and dimension
            }
        }
        print id, y, x, z;  # print coordinates
    }

A general block of a gawk program consists of two parts a pattern and a code
block. Usually `regular expressions <regexp.rst>`_ are used in the pattern. 
The *BEGIN* 
pattern is similar to the *END* pattern we used before, but it is executed 
once, before the processing starts. Copy the code above into the *m52coo.awk* 
file. Let's convert *sample.m5* file to a coordinate list.

.. code:: bash

    gawk -f m52coo.awk sample.m5 > sample.txt

Text positions and other data from a DXF file
---------------------------------------------

DXF (Drawing eXchange Format) is a very popular CAD data exchange format and
several CAD/GIS software can read/write it. We'll collect information from
such file about the TEXT entities (position, direction, size and the text 
itself)

.. code:: gawk
    BEGIN {
        print "EAST;NORTH;LAYER;DIRECTION;SIZE;TET";  # print header
    }
    /^ENTITIES/,/^EOF/ {
        if ($0 == "  0") {                  # next entity reached
            if (entity == "TEXT") {         # output text data
                printf("%.2f;%.2f;%.5f;%.2f;%s\n", x, y, layer, angle, size,  txt);
            }
            entity = ""; txt = ""; angle = 0; size = 1; layer = ""
            last = "";                      # initialize variables
        }
        if (last == "  0") { entity = $0; } # actual entity type
        if (last == "  8") { layer = $0; }  # layer
        if (last == " 10") { x = $0; }      # east  
        if (last == " 20") { y = $0; }      # north
        if (last == " 40") { size = $0; }   # text size
        if (last == " 50") { angle = $0; }  # text direction
        if (last == "  1") { txt = $0; }    # text
        last = $0;                          # last input line
    }

The end of line (EOL) character(s) are different on Linux and Windows boxes.
When you use gawk you have to convert the EOL to the standard of the used
operating system. To convert Windows text files to Linux use dos2unix command.

.. code:: bash

    dos2unix your_text_file

The different text files may use different code pages. You can convert text
files between code pages (for example from UTF-8 to ISO8859-2) using iconv
Linux utility.

.. code:: bash

    icov -f source_code_page -t target_code_page source_file > target_file
