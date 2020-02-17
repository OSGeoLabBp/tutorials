Observation processing using GAWK, Octave and Python/numpy
==========================================================

    :Authors: **Zoltan Siki** <siki.zoltan@epito.bme.hu>
    :Version: 1.0

Preface
-------

GNU AWK (named after the creators Aho, Weinberger and Kernighan) is a 
Unix/Linux programable text utility what is compiled for Windows platforms, too.
The GAWK program syntax is similiar to C language.

GNU Octave is an open source high-level interpreted language, primarily 
intended for numerical computations. The syntax of the Octave program is 
quite similiar to Matlab, you can easy port programs between GNU Octave and
Matlab.

Python is nowadays one of the most popular programming languages. It has several
extension modules.
Numpy modul adds the power to numeric processing to Python.

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
*	extending Python/numpy knowledge

Table of contents
-----------------

#. `Load coordinates from Leica GSI into QGIS or AutoCAD <lessons/leica_gsi.rst>`_ (gawk, Octave)
#. `Processing GSI file got from Leica DNA03 digital level <lessons/leica_dna03.rst>`_ (Octave)
#. `Converting GPX to KML <lessons/gpx.rst>`_ (QGIS, ogr2ogr, Python)
#. `NMEA message processing and display <lessons/nmea.rst>`_ (gawk, Octave, Python)
#. `Processing observations for a moving point <lessons/one_point.rst>`_ (Octave)
#. `Measure point with slope prism rod <lessons/sphere.rst>`_ (Octave)
#. `Processing LiDAR data <lessons/lidar.rst>`_ (Octave)
#. `Monitoring data processing <lessons/monitoring_data.rst>`_ (Octave)
#. `Level network adjustment and data snooping <lessons/level_net.rst>`_ (Octave, Python)
#. `Propagation of errors for polar observations <lessons/propagation_of_error.rst>`_ (OCtave)
#. `Coordinate list processing with Unix text file utilities <lessons/coord_list.rst>`_
#. `Statistics from NMEA file <lessons/nmea_stat.rst>`_ (OCtave, Python)
#. `Polynom interpolation <lessons/polinom.rst>`_ (Octave, Python)
#. `Generalised inverse <lessons/pseudo_inverz.rst>`_ (Octave)
#. `Regression circle <lessons/circle.rst>`_ (Octave)
#. `Generate report from a DXF file <lessons/dxfinfo.rst>`_ (gawk)
#. `Find prime numbers <lessons/prime.rst>`_ (Octave, Python)
#. `Section from point cloud <lessons/lidar_section.rst>`_ (gawk, Octave)
#. `Regression sphere <lessons/reg_sphere.rst>`_ (Octave)
#. `Bulk extract GPS positions from images <lessons/exif.rst>`_ (shell script, gawk, Python)
#. `Bulk image convert to GeoTiff <lessons/image2geotiff.rst>`_ (shell script, gdal)
#. `3D ortogonal transformation <lessons/3dtr.rst>`_ (Octave)
#. `Processing bridge deflection data <lessons/deflection.rst>`_ (Octave)
#. `Download RINEX navigation files and count ephemeris of different satellite systems <lessons/numephem.rst>`_ (shell script, gawk)


Program codes and sample data are in the `code <code>`_ folder.


