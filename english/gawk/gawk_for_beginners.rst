gawk for beginners
==================

gawk (GNU awk) is a programable unix text utility. It is one of the most complex
of them. Several simple examples will be introduced to teach you by examples.

gawk processes the input text file line by line. Each line is divided into
fields using a set of field separators. The default field separators are *TAB* 
and *space*.  We can refere to a field in the actual line by its ordinal
number e.g. $1 (first field),
$2 (second field), etc. $0 gives the whole actual input line.

There are some variables maintained by gawk. The most important ones are:

* *NF* number of fields in the actual input line
* *NR* row number in input file
* *FS* field separator(s)

The gawk program can be given in the command line if it is very short or we
can create a separate file for the program. The usual extension for gawk
program file is *.awk*.

gawk reads data from the input file or from the standard input line by line,
processes the input and prints output to the standard output.

The syntaxis of the gawk programs are very similiar to C programs. gawk can be 
a good start point to learn C.

A *gawk* program consists of pattern and action pairs. The pattern must match
the actual input line to trigger the action. All matching actions are 
evaluated, not only the first!

There are some kinds of patterns:

* Regexp pattern: a regular expression e.g. /^[0-9]+/
* Expression pattern: any expression e.g. NF > 4
* Range: pairs of patterns specif record range e.g. /^ENTITIES/, /^ENDSEC/
* BEGIN: special pattern to initialize
* END: special pattern to clean up
* empty: the empty pattern mathes every input line

After the pattern the action have to be put into a code block. Code blocks are 
delimited by curly bracket "{" and "}".

Add row numbers to a text file
------------------------------

.. code:: gawk

    gawk '{ print NR, $0 }' /etc/passwd

The example above will print back the Linux password file with line numbers to
the standard output. The output of the gawk command can be redirected to 
the a file e.g.

.. code:: gawk

    gawk '{ print NR, $0 }' /etc/passwd > row_num_passwd

.. note::

    In the command line single quotes have to be used to hide $ for bash
    to interprete

Remove columns from input file
------------------------------

.. code:: bash

   gawk -F: '{ print $1, $3, $5 }' /etc/passwd

The example above will print out the Linux user names, user ID and full name.
After the -F switch a custom field separator can be defined. The *cut* command
can be used to generate the same output.

.. code:: bash

    cut -d: -f 1,3,5 /etc/passwd

Reverse the field order of the input lines
------------------------------------------

.. code:: gawk

    { for (i = NF; i > 0; i--) { printf "%s:", $i; }
      printf "\n";
    }

The *for* command is to count iterations. *i* is the loop variable and changed
from the number of fields (*NF*) down to *1*. We can refere to the *ith* field
by *$i*. *printf* is for formatted print, it won't print new line at the end.
*printf "\\n";* prints a new line character (*print ""* would be good too).

This case we create a separate file for the gawk program. Copy the program
above into a file called *reverse.awk*. Then use the following commad to run
this gawk program.

.. code:: bash

    gawk -F : -f reverse.awk /etc/passwd

-F switch to define field separator and -f to give the name of the program file.

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
sort the file before using *unique.awk*. The pipe character ("|") redirects
the output of the left side command to the input of the right side one.

.. note::

    The sort Linux command has -u switch to output unique values.
	e.g. gawk -F : '{ print $NF; }' /etc/passwd | sort -u

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

Simple examples to handle coordinate list
-----------------------------------------

*sample.txt* file will be used during the following examles, you can find this file in
the code subdirectory. Each row in the file contains point ID, easting, northing and
optional elevation. Let's find all the point numbers starting by 3.

.. code:: gawk

    gawk '/^3/' sample.txt

.. note::

    The Linux grep utility can also be used to filter lines.
    e.g. grep '^3' sample.txt

Let's print out lines between the 15th and 21th lines.

.. code:: gawk

    gawk 'NR >= 15 && NR <= 21' sample.txt

.. note::

    Linux head and tail command can solve the same question.
	e.g. tail -n +15 sample.txt | head -n 7

Let's find rows having no eleveation.

.. code:: gawk

    gawk 'NF < 4' sample.txt

Lets's find rows having point ID between 305 and 316.

.. code:: gawk

    gawk '$1 >= 305 && $1 <= 316' sample.txt

Let's create a new coordinate list file where only easting and northing
coordinates are listed with two decimals. Let's skip lines if point ID
is non mumerical.

.. code:: gawk

    $1 ~ /^[0-9]+$/ { printf("%d,%.2f,%.2f\n", $1, $2, $3) }

Input the code above into the *twod.awk* file.

.. code:: bash

    gawk -f twod.awk sample.txt

Let's calculate the average of the horizontal co-ordinates for point 
number groups (1st group 100-199, second group 200-299, etc.).

.. code:: gawk

	/^1[0-9]{2} / { sum_x[1] += $2; sum_y[1] += $3; n[1]++; }
	/^2[0-9]{2} / { sum_x[2] += $2; sum_y[2] += $3; n[2]++; }
	/^3[0-9]{2} / { sum_x[3] += $2; sum_y[3] += $3; n[3]++; }
	/^4[0-9]{2} / { sum_x[4] += $2; sum_y[4] += $3; n[4]++; }
	/^5[0-9]{2} / { sum_x[5] += $2; sum_y[5] += $3; n[5]++; }
	/^6[0-9]{2} / { sum_x[6] += $2; sum_y[6] += $3; n[6]++; }
	END { for (i = 1; i < 7; i++) {
			printf("%d00-%d99: %.3f, %.3f\n", i, i, sum_x[i] / n[i], sum_y[i] / n[i]);
		}
	}

Enter the code into *average.awk* file.

.. code:: bash

	gawk -f average.awk sample.txt

A shorter and more general version for all 3 digit point numbers:

.. code:: gawk

	/^[1-9][0-9]{2} / { i = int($1 / 100);  # array index
			sum_x[i] += $2; sum_y[i] += $3; n[i]++; }
	END { for (i in n) {
			printf("%d00-%d99: %.3f, %.3f\n", i, i, sum_x[i] / n[i], sum_y[i] / n[i]);
		}
	}

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
several CAD/GIS software can read/write it, but TEXT and MTEXT entities are not
handled perfectly.
We'll collect information from such file about the TEXT and MTEXT entities
(position, direction, size and the text itself) into a CSV file. 

Sample DXF with TEXT entity:

.. code:: text

    SECTION
      2
    ENTITIES
      0
    TEXT
      5
    2048C
    330
    1F
    100
    AcDbEntity
      8
    STREETNAMES
      6
    CONTINUOUS
     62
         8
    100
    AcDbText
     10
    90.964720896096
     20
    198.89131946725
     30
    0.0
     40
    3.0
      1
    Bihari utca
     50
    42.804


.. code:: gawk

    BEGIN {
        print "EAST;NORTH;LAYER;DIRECTION;SIZE;TEXT";   # print header
        rad2deg = 180.0 / atan2(1.0, 1.0) / 4;
    }
    /^ENTITIES/,/^EOF/ {
        if ($0 == "  0") {                  # next entity reached
            if (entity == "MTEXT") {        # calculate angle from dx, dy
                angle = atan2(dy, dx) * rad2deg;    # angle in deg
            }
            if (entity == "TEXT" || entity == "MTEXT") {    # output text data
                printf("%.2f;%.2f;%s;%.5f;%.2f;%s\n", x, y, layer, angle, size, txt);
            }
            entity = ""; txt = ""; angle = 0; size = 1; layer = "";
            dx = dy = 0.0;
            last = "";                      # initialize variables
        }
        if (last == "  0") { entity = $0; } # actual entity type
        if (last == "  8") { layer = $0; }  # layer
        if (last == " 10") { x = $0; }      # east  
        if (last == " 20") { y = $0; }      # north
        if (last == " 11") { dx = $0; }     # direction for MTEXT   
        if (last == " 21") { dy = $0; }     # direction for MTEXT
        if (last == " 40") { size = $0; }   # text size
        if (last == " 50") { angle = $0; }  # text direction
        if (last == "  1") { txt = $0; }    # text
        last = $0;                          # last input line
    }

Let's convert texts from sample.dxf into a text file (texts.txt).

.. code:: bash

	gawk -f dxf_txt2csv.awk sample.dxf > texts.txt

The end of line (EOL) character(s) are different on Linux and Windows boxes.
When you use gawk you have to convert the EOL to the standard of the used
operating system. To convert Windows text files to Linux use dos2unix command.

.. code:: bash

    dos2unix your_text_file

The different text files may use different code pages. You can convert text
files between code pages (for example from UTF-8 to ISO-8859-2) using iconv
Linux utility.

.. code:: bash

    iconv -f source_code_page -t target_code_page source_file > target_file
