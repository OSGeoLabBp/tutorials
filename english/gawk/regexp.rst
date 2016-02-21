Regular expressions
===================

By the help of regular expressions (regepx) diserve text patterns can be defined
Regexp are used by most of the Linux text processing utilities (e.g. grep, awk,
sed) and text editors (vi, emacs). Here is a vwry short and incomplete list
of special regexp characters:

.. code:: text

    .         (dot) any character except new line
    ^         beginning of the line
    $         end of the line
    [abc]     one character from the set in the brackets
    [^abc]    one character not in the set in brackets
    [a-z]     one character from the interval in brackets (inclusive)
    [^a-z]    one character not in the set in brackets
    ( )       make group in pattern
    {min,max} repetition of the previous character or group, max part is optional
    p1 | p2   p1 pattern or p2 pattern
    p *       any number of repetition of p pattern, including zero equivalent to p{0,}
    p+        one or more repetition of p pattern, equivalent to p{1,}
    p?        zero or one repetition of p pattern, equivalent to p{0,1}
    \         escape the special meaning of the next character (e.g. \. the dot character, not any character)

Example regular expression
 
.. code:: text

    contains the word "apple"  
    regexp: alma
    matching text: an apple on the table

    begins with the word "apple"
    regexp: ^apple
    matching text: apple on the table
    
    exactly the world "apple"
    regexp: ^apple$
    matching text: apple

    begins with the word "apple" and ionly any number of spaces after
    regexp: ^apple *$
    matching text: apple    

    begins with character "a" and contains 5 characters
    regexp: ^a....$ or ^a.{4}$
    matching text: apple

    begins with character "a" or "A" and contains 5 characters
    regexp: ^[aA].{4}$
    matching text: Apple

    there is a letter in the text
    regexp: [a-z]|[A-Z]
    matching text: ApPlE

   integer number with sign
   regexp: ^[-+]?[0-9]+$
   matching text: -0000123

   integer number, no leading zeros
   regexp: ^0|([-+]?[1-9][0-9]*)$
   matching text: 123
  
   float number with exponetial part (e.g. -1.234e-7)
   regexp: ^-?[0-9]+\.?[0-9]*([eE][+-]?[0-9]*)?$
   matching text: -1.234E-5
  
   angle in DMS (e.g. 23-34-45)
   regexp: ^[0-9]([0-9]){0,2}(-[0-9][0-9]?){0,2}$
   matching text: 102-02-31

   valid email address
   regexp: ^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*$
   matching text: siki.zoltan@epito.bme.hu
