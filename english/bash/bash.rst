Introduction to bash programming
================================

This tutorial introduces bash basics for beginners. 

Hello world
-----------

Let's write the usual first program in any language, which writes "Hello world"
string to the screen. Use any simple text editor (e.g. vi, gedit, pico, ...)
to create hello.sh file and input the following two lines.

.. code:: bash

	#!/bin/bash
	echo "Hello world"

The first line is the so called shebang, It tells the operating system use
bash to run this script.

Starting the script at the bash prompt:

.. code:: bash

	~$ bash hello.sh
	Hello world
	~$ . hello.sh
	Hello world
	chmod +x hello.sh
	./hello.sh
	Hello world

The first and second line start bash and the parmeter is the name of the script.
In the third line the executable flag is added to the file. After it the script
name is enough (and the sheband) to run the script.

.. note::

	The *chmod* command should be used once for a file.

Variables
---------

Variables are created by assigment a value to it.

.. code:: bash

	~$ hello="Hello world"

The value of the variable can be accessed inserting \$ in front of the variable
name.

.. code:: bash

	~$ echo $hello
	Hello world

The *hello* variable is local to this shell. To create global variables (which
are accessible in the subshells) use export in front of the assignment.
Double and single quotes are different in shells. Between double quotes
variable substitution is done.

.. code:: bash

	~$ echo "$hello, I am Jack"
	Hello world, I am Jack
	~$ echo '$hello, I am Jack'
	$hello, I am Jack

Curly braces are used to separate variable name if neccessary.

.. code:: bash

	~$ echo ${hello}s
	Hello worlds
	~$ echo "${hello}s"
	Hello worlds

The use of double quotes in the echo command is not obligatory.

.. note::

	In the variable assignment no space allowed before and after the 
	assignment operator (=). For example *a = 12* doesn't work.

Loops
-----

Let's write script to list file names in the current directory

.. code:: bash

	#!/bin/bash
	for i in *		# for i in $(ls)  or   for i in `ls` is the same
	do
		echo $i
	done

In the shell scripts the bash wild card characters (* and ?) are substituted as
in any bash command at the command prompt. Instead of "*" we could use
$(ls) or \`ls\` as it is mentioned in the comment (after # till the end of
line you can write comments).

Using the *seq* command a counter can be used in the loop variable. Let's
write a script to add the first 10 whole numbers (sum.sh).

.. code:: bash

	#!/bin/bash
	s=0
	for i in `seq 1 10`; do
		let s=$s+$i			# `expr $s + $i`  or  $(($s+$i))  is the same
	done
	echo $s

In the previous example ";" was used to sepatete two commands in the same line.
The *seq 1 10* generates the integer numbers from 1 to 10. Note that the bash
can make integer aritmetics after *let*. Let's try our script.

.. code:: bash

	~$ . sum.sh
	55

.. note::

	There are *while* and *until* loops in bash, too.

Let's make our sum script more fexible, get the upper limit of the sum from the
command line. Create sum1.sh file and insert the following script.

.. code:: bash

	#!/bin/bash
	s=0
	for i in `seq 1 $1`; do
		s=$(($s+$i))
	done
	echo $s
	
The *$1* is substituted by the first command line parameter. *$2* is for the
value of the second command line parameter.
Let's test our script.

.. code:: bash

	~$ chmod +x sum1.sh
	~$ ./sum1.sh 50
	1275
	~$ ./sum1.sh
	1
	~$ ./sum1.sh 10 20 30
	55

Note that the result is false if no parameter is given and if more parameters
are given, only the first is considered.

Conditionals
------------

Let's extend the previous sum example to check the number of parameters.

.. code:: bash

	#!/bin/bash
	if [ $# -ne 1 ]; then
		echo Invalid number of parameters
		echo usage: sum2.sh n
		exit 1
	fi
	s=0
	for i in `seq 1 $1`; do
		s=$(($s+$i))
	done
	echo $s

The *$#* substituted by the number of parameters. In the *if* command add a
space before and after square brackets.

.. note::

	Other relational operators are available: -ne is not equal, -gt is 
	greater, -le is less or equal, etc.

Let's try the modified script.

.. code:: bash

	~$ chmod +x sum2.sh
	~$ ./sum2.sh 
	Invalid number of parameters
	usage: sum2.sh n
	~$ ./sum2.sh 10 20 30
	Invalid number of parameters
	usage: sum2.sh n
	~$ ./sum2.sh 5
	15

Let's make one more extension on our script. Calculate the sum for all
command line parameters (sum3.sh).

.. code::

	#!/bin/bash
	if [ $# -lt 1 ]; then
		echo Invalid number of parameters
		echo usage: sum2.sh n1 n2 ...
		exit 1
	fi
	for j in $*; do
		s=0
		for i in `seq 1 $j`; do
			s=$(($s+$i))
		done
		echo $s
	done

The $\* means all the command line parameters. Let's try the script.

.. code:: bash

	~$ chmod +x sum3.sh
	~$ ./sum3.sh 
	Invalid number of parameters
	usage: sum2.sh n1 n2 ...
	~$ ./sum3.sh 10 20 30
	55
	210
	465
