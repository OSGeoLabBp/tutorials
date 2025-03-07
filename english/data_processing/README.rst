Geodata processing using Python/numpy, GAWK and Octave
======================================================

    :Authors: **Zoltan Siki** <siki.zoltan@emk.bme.hu>, **Bence Takacs** <takacs.bence@emk.bme.hu>
    :Version: 1.1

Preface
-------

Python is nowadays one of the most popular programming languages. It has several
extension modules.
Numpy, scipy and pandas modules add the power of numeric processing to Python. 
See some elementary lessons for Python:

* `Python in a nutshell <lessons/python_in_a_nutshell.ipynb>`_ a Jupyter notebook for beginners in Python
* `Command line arguments <lessons/commandlineparameters.ipynb>`_ a Jupyter notebook
* `Numpy in a nutshell <../python/numpy_tutor.ipynb>`__ a Jupyter notebook
* `Vectorization <../python/vectorization.ipynb>`__ a Jupyter notebook
* `Pandas in a nutshell <../python/pandas_tutor.ipynb>`__ a Jupyter notebook
* `Regular expressions in Python <../python/regexp_in_python.ipynb>`__ a Jupyter notebook
* `Pylint <../python/pylint.ipynb>`__ beautify your Python code, a Jupyter notebook

Many Python lessons are written in Jupyter notebook on Google Colab. You can 
open them even if you have no Google account. These lessons have an **Open in 
Colab** link at the beginning. Click on it and you can try and edit the notebook
(for editing you have to login to Google).

Samples mostly concern on observation data/file processing.

GNU AWK (named after the creators Aho, Weinberger and Kernighan) is a 
Unix/Linux programable text utility what is compiled for Windows platforms, too.
The GAWK program syntax is similiar to C language.

GNU Octave is an open source high-level interpreted language, primarily 
intended for numerical computations. The syntax of the Octave program is 
quite similiar to MATLAB, you can easy port programs between GNU Octave and
MATLAB (see the table at the end of this page.

Samples were tested on Linux and Google colab, but should run on other environments, too.

Table of contents
-----------------

File processing

#. `Text file processing in Python <lessons/text_files.ipynb>`_ (Jupyter notebook)
#. `Convert GSI data to CAD drawing <lessons/GSI2DXF.ipynb>`_ (Jupiter notebook)
#. `Generate report from a DXF file <lessons/dxfinfo.ipynb>`_ (Jupyter notebook)
#. `Convert binary file to text file <lessons/binary_file.ipynb>`_ (Jupyter notebook)
#. `Load coordinates from Leica GSI into QGIS or AutoCAD <lessons/leica_gsi.rst>`_ (gawk, Octave, Python)
#. `Processing GSI file got from Leica DNA03 digital level <lessons/leica_dna03.rst>`_ (Octave)
#. `Converting GPX to KML <lessons/gpx.rst>`_ (QGIS, ogr2ogr, Python)
#. `Coordinate list processing with Unix text file utilities <lessons/coord_list.rst>`_
#. `Generate report from a DXF file <lessons/dxfinfo.rst>`_ (gawk)

GNSS

#. `NMEA files processing <lessons/nmea.ipynb>`_ (Jupyter notebook)
#. `Download navigational RINEX file from IGS data center <lessons/download_gnss_data.ipynb>`_ (Jupyter notebook)
#. `Run RTKLIB from a python script <lessons/rtklib_python.ipynb>`__ (Jupyter notebook)
#. `Statistics from NMEA file <lessons/nmea_stat.rst>`_ (Octave, Python)
#. `NMEA message processing and display <lessons/nmea.rst>`_ (gawk, Octave, Python)
#. `Download RINEX navigation files and count ephemeris of different satellite systems <lessons/numephem.rst>`_ (shell script, gawk)

Point cloud data

#. `Point cloud section <lessons/point_cloud_section.ipynb>`_ (Jupyter notebook)
#. `Find plane in a point cloud <lessons/ransac_plane.ipynb>`_ (Jupyter notebook)
#. `Finding spheres in a point cloud <lessons/ransac_sphere.ipynb>`_ (Jupyter notebook)
#. `GRID from LiDAR data <lessons/grid.ipynb>`_ (Jupyter notebook)
#. `Filter point cloud <lessons/pc_filter.rst>`_ (gawk, Python, CloudCompare)
#. `Processing LiDAR data <lessons/lidar.rst>`_ (Octave, Python)
#. `DTM GRID from point cloud <lessons/pc2grid.rst>`_ (Python, Octave)
#. `Section from point cloud <lessons/lidar_section.rst>`_ (gawk, Octave, Python)

Time series

#. `Processing sensor data for Structural Health Monitoring <lessons/shm.rst>`_ (Jupyter notebooks)
#. `Signal processing example using scipy, pandas and matplotlib <lessons/spectral.ipynb>`_ (Jupyter notebook)
#. `Processing observations for a moving point <lessons/one_point.rst>`_ (Octave)
#. `Processing bridge deflection data <lessons/deflection.rst>`_ (Octave)
#. `Monitoring data processing <lessons/monitoring_data.rst>`_ (Octave, Python)

Clustering, interpolation, regression and transformation

#. `Clustering with Machine Learning <lessons/ml_clustering.ipynb>`__ (Jupyter notebook)
#. `RANSAC line in 2D <lessons/ransac_line.ipynb>`_ (Jupyter notebook)
#. `Robust 2D transformation <lessons/trans.ipynb>`__ (Jupyter notebook)
#. `Regression circle/ellipse & RANSAC circle/ellipse <lessons/circle.ipynb>`_ (Jupyter notebook)
#. `Principal Component Analysis (PCA) <lessons/pca.ipynb>`_  (Jupyter notebook)
#. `Polynom interpolation and regression <lessons/polinom.rst>`_ (Octave, Python)
#. `Regression circle <lessons/circle.rst>`_ (Octave, Python)
#. `Regression sphere <lessons/reg_sphere.rst>`_ (Octave, Python)
#. `3D ortogonal transformation <lessons/3dtr.rst>`_ (Octave, Python)
#. `Principal Component Analysis (PCA) <lessons/pca.rst>`_ (Python, Octave)

Images

#. `Movement and deformation analysis from images <lessons/img_def.ipynb>`_ (Jupyter notebook)
#. `Digital image processing <../img_processing/img_proc.ipynb>`_ (Jupyter notebook)
#. `Bulk extract GPS positions from images <lessons/exif.rst>`_ (shell script, gawk, Python)
#. `Bulk image convert to GeoTiff <lessons/image2geotiff.rst>`_ (shell script, gdal, Python)
#. `Create image mosaic <lessons/img_mosaic.rst>`_ (shell script, Python)
#. `Find circles in an image <lessons/find_circle.rst>`_ (Python)

Surveying calculation

#. `Measure point with slope prism rod <lessons/sphere.rst>`_ (Octave)
#. `Generalised inverse <lessons/pseudo_inverz.rst>`_ (Octave, Python)
#. `Level network adjustment and data snooping <lessons/level_net.rst>`_ (Octave, Python)
#. `Free horizontal network adjustment <lessons/horiz_net.rst>`_ (Octave)
#. `Propagation of errors for polar observations <lessons/propagation_of_error.rst>`_ (OCtave)

Mixed

#. `Create time/data plot <lessons/time_data_plot.rst>`_ (Python)
#. `Find prime numbers <../python/effective_algorithms.ipynb>`_ (Jupyter notebook)
#. `Find prime numbers <lessons/prime.rst>`_ (Octave, Python)

Program codes and sample data are in the `code <lessons/code>`_ folder.


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
