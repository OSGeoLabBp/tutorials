Tutorials using OpenCV and Python
=================================

#. `Common image processing tasks <img_proc.ipynb>`_ (Jupyter notebook)
#. `Movement and deformation analysis from images <../data_processing/lessons/img_def.ipynb>`_ (Jupyter notebook)

Sample programs in code folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Image correlation
-----------------

Find template image in the reference image (code/img_correlation.py)

  Usage: img_correlation.py method_id template image gui
      method_id - 0/1/2/3 CV_TM_SQDIFF_NORMED/CV_TM_CCORR_NORMED/CV_TM_CCOEFF/CV_TM_CCOEFF_NORMED
      
      template  - template image to find in the reference image
      
      image     - reference image
      
      gui       - draw image mark match
      
      img_correlation.py 0 mona_temp4.png monalisa.jpg gui

Histogram equalization
----------------------

Equalize image histogram to a reference image using Scikit (code/image_equalize.py).

  usage: image_equalize.py [-h] -r REFERENCE [--nowrite] [--debug]
                         [file_names [file_names ...]]

  positional arguments:
    file_names            pathes image files to process

  optional arguments:
    -h, --help            show this help message and exit
    -r REFERENCE, --reference REFERENCE
                          path to the input reference image
    --nowrite             do not write equalized images to disk
    --debug               show images on screen

