Observation processing using GAWK and Octave
============================================

    :Authors: **Zoltan Siki** <siki.zoltan@epito.bme.hu>
    :Version: 1.0

Preface
-------

GNU AWK (named after the creators Aho, Kernighan, and Weinberger) is a 
Unix/Linux programable text utility what is compiled for Windows platforms, too.
The GAWK program syntax is similiar to C language.

GNU Octave is an open source high-level interpreted language, primarily 
intended for numerical computations. The syntax of the Octave program is 
quite similiar to Matlab, you can easy port programs between GNU Octave and
Matlab.

Samples mostly concern on observation data/file processing.

Samples were tested on Linux but should run on a Windows box, too.
Octave .m files may need some editing to run with Matlab. We sum up some
incompatibilities between Octave and Matlab in the following table.

+--------------------------+---------------------+---------------------+
| **Operation**            | **Octave**          | **Matlab**          |
+==========================+=====================+=====================+
| Denial                   | !                   | ~                   |
|                          | *or*                |                     |
|                          | ~                   |                     |
+--------------------------+---------------------+---------------------+
| Not equal                | !=                  | ~=                  |
|                          | *or*                |                     |
|                          | ~=                  |                     |
+--------------------------+---------------------+---------------------+
| Increment                | i++                 | i = i + 1           |
|                          | *or*                |                     |
|                          | i += 1              |                     |
|                          | *or*                |                     |
|                          | i = i + 1           |                     |
+--------------------------+---------------------+---------------------+
| Power                    | ^                   | ^                   |
|                          | *or*                |                     |
|                          | **                  |                     |
+--------------------------+---------------------+---------------------+
| Standard output          | printf('Hello')     | fprintf('Hello')    |
|                          | *or*                |                     |
|                          | fprintf('Hello')    |                     |
+--------------------------+---------------------+---------------------+
| String constants         | "Hello"             | 'Hello'             |
|                          | *or*                |                     |
|                          | 'Hello'             |                     |
+--------------------------+---------------------+---------------------+
| String search            | index(str, sample)  | strfind(str, sample)|
|                          | *or*                |                     |
|                          | strfind(str, sample)|                     |
|                          | *or*                |                     |
|                          | findstr(str, sample)|                     |
+--------------------------+---------------------+---------------------+
| End of code block        | end                 | end                 |
|                          | *or*                |                     |
|                          | endif               |                     |
|                          | endwhile            |                     |
|                          | endfunction         |                     |
+--------------------------+---------------------+---------------------+
| Comment                  | \#                  | %                   |
|                          | *or*                |                     |
|                          | %                   |                     |
+--------------------------+---------------------+---------------------+
| Comment block            | \%\{                | \%\{                |
|                          | ...                 | ...                 |
|                          | %\}                 | %\}                 |
|                          | *or*                |                     |
|                          | \#{                 |                     |
|                          | ...                 |                     |
|                          | \#}                 |                     |
+--------------------------+---------------------+---------------------+
| Line continuation        | ...                 | ...                 |
| (at the end of line)     | *or*                |                     |
|                          | \\                  |                     |
+--------------------------+---------------------+---------------------+

If you would like to use a script in Matlab, too use Octave with the
*--traditional* command line switch. This way you will get warnings in case of
Matlab incompatible structures.

*Topics covered*

*   using pipelines, redirecting standard input and output (Unix/DOS)
*   using simple text processing utilities (grep, gawk, etc.)
*   using file input/output
*   using variables, expressions, decision control (conditional statement, loops), functions
*   using regular expressions
*   extending Octave/Matlab knowledge
*   vectorization

Table of contents
-----------------

#. `Load coordinates from Leica GSI into QGIS or AutoCAD <lessons/leica_gsi.rst>`_
#. `Processing GSI file got from Leica DNA03 digital level <lessons/leica_dna03.rst>`_
#. `Converting GPX to KML <lessons/gpx.rst>`_
#. `NMEA message processing and display <lessons/nmea.rst>`_
#. `Processing observations for a moving point <lessons/one_point.rst>`_
#. `Measure point with slope prism rod <lessons/sphere.rst>`_
#. `Processing LiDAR data <lessons/lidar.rst>`_
#. `Monitoring data processing <lessons/monitoring_data.rst>`_
#. `Level network adjustment and data snooping <lessons/level_net.rst>`_
#. `Propagation of errors for polar observations <lessons/propagation_of_error.rst>`_
#. `Coordinate list processing with Unix text file utilities <lessons/coord_list.rst>`_
#. `Statistics from NMEA file <lessons/nmea_stat.rst>`_
#. `Polynom interpolation <lessons/polinom.rst>`_
#. `Generalised inverse <lessons/pseudo_inverz.rst>`_
#. `Regression circle <lessons/circle.rst>`_
#. `Generate report from a DXF file <lessons/dxfinfo.rst>`_
#. `Find prime numbers <lessons/prime.rst>`_
#. `Section from point cloud <lessons/lidar_section.rst>`_
#. `Regression sphere <lessons/reg_sphere.rst>`_
#. `Bulk extract GPS positions from images <lessons/exif.rst>`_
#. `Bulk image convert to GeoTiff <lessons/image2geotiff.rst>`_
#. `3D ortogonal transformation <lessons/3dtr.rst>`_
#. `Processing bridge deflection data <lessons/deflection.rst>`_
#. `Download RINEX navigation files and count ephemeris of different satellite systems <lessons/numephem.rst>`_


Program codes and sample data are in the `code <code>`_ folder.


