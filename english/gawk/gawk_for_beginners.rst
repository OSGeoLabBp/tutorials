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

.. code:: gawk

    BEGIN {
        FS = "[\|]";    # field separator
    }

    /\|Y / {            # y coordinate given in thi line
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
block. Usually regular expressions is used in the pattern. The *BEGIN* 
pattern is similar to the *END* pattern, but is is executed once, before the 
processing starts. Copy the code above into the *m52coo.awk* file.
Lest's convert *sample.m5* file to a coordinate list.

.. code:: bash

    gawk -f m52coo.awk sample.m5 > sample.txt
