Find circles in an image
========================

*Keywords:* python, OpenCV

*Program file:* hsv.py

Let's try to find red circles in an image. First we mask out everything what is not red.
We can do it if the image is converted to HSV color-space. OpenCV has a *cvtColor*
function to change color-space. 

.. note:: Color-spaces

    There are some color-spaces used in computer graphic. The best known is the RGB
    (Red/Green/Blue) which is used by monitors. Printers uses CYM (Cian/Yellow/Magenta).
    For some image processing algorithms a HSV (Hue/Saturation/Value) color-space is
    prefered. OpenCv uses the BGR (BLue/Green/Red) color-space.

.. code:: python

    hsv_image = cv2.cvtColor(source, cv2.COLOR_BRG2HSV)

The next step to create a mask for the different shades of red. We can use *inRange*
function create a mask for a range of colors. This range have to be defined in HSV
color-space, too. *bgr2shv* is a simple function which converts a color vector of 
BGR values to HSV, see the codeat the bottom of the page.

.. code:: python

    c1 = np.uint8([0, 0, 10])
    c2 = np.uint8([0, 0, 255])

    image_mask = cv2.inRange(hsv_image, bgr2hsv(c1), bgr2hsv(c2))

Then the must is applied for the source image, to preserve only the red pixels.

.. code:: python

    img = cv2.bitwise_and(source, source, mask=image_mask)

It a bit tricky, the function makes a bitwise and with the image itself, which gives 
back the original image but the musk is also applied, so finally we get areas.

Outside the mask white color is preserved other colors are change to black. We change
black pixels to white.

.. code:: python

    img[image_mask == 0] = np.array([255,255,255])

In OpenCv the Hough circle search algorithm is implemented. It can be used for gray-scale 
images, so we have to convert the masked BGR image to gray-scale

.. code::

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

Finaly we call
the HoughCircles function for the masked gray image to find all circles.

.. code:: python

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)


Here is a complex program to find red circles in the input video stream or in the
imput images given in the command line.

.. code:: python

    """
        Image filters
    """
    import numpy as np
    import cv2

    def rbg2hsv(col):
        """ Convert RGB to HSV color space 
            :param col: list of 3 int between 0-255 or an np array
        """
        return cv2.cvtColor(np.array([[col]], dtype=np.uint8),
                            cv2.COLOR_RGB2HSV)[0][0]

    def rgb2bgr(col):
        """ Convert RGB to BGR color space 
            :param col: list of 3 int between 0-255 or an np array
        """
        return cv2.cvtColor(np.array([[col]], dtype=np.uint8),
                            cv2.COLOR_RGB2BGR)[0][0]

    def bgr2hsv(col):
        """ Convert BGR to HSV color space 
            :param col: list of 3 int between 0-255 or an np array
        """
        return cv2.cvtColor(np.array([[col]], dtype=np.uint8),
                            cv2.COLOR_BGR2HSV)[0][0]

    def color_filter(frame, c1, c2):
        """ filter colors between c1 and c2
            c1 and c2 have to be given OpenCV HSV

            :param frame: BGR image
            :param c1: BGR color to filter from
            :param c2: BGR color to filter to
        """
        # convert image to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        image_mask = cv2.inRange(hsv, bgr2hsv(c1), bgr2hsv(c2))
        img = cv2.bitwise_and(frame, frame, mask=image_mask)
        # change black to white outside mask
        img[image_mask == 0] = np.array([255,255,255])
        return img

    if __name__ == "__main__":
        from sys import argv

        red1 = np.uint8([0, 0, 10])
        red2 = np.uint8([0, 0, 255])

        if len(argv) == 1:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                img = color_filter(frame, red1, red2)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
                if circles:
                    circles = np.uint16(np.around(circles))
                    # draw circles on image
                    for i in circles[0,:]:
                        cv2.circle(img, (i[0], i[1]), i[2], (0,255,0), 4)
                cv2.imshow('Output', img)
                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()
            cap.release()
        else:
            for name in argv[1:]:
                frame = cv2.imread(name)
                img = color_filter(frame, red1, red2)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.5, 50)
                if circles is None:
                    print('No circles found')
                else:
                    circles = np.uint16(np.around(circles))
                    # draw circles on image
                    for i in circles[0,:]:
                        cv2.circle(img, (i[0], i[1]), i[2], (0,255,0), 4)
                        print(i[0], i[1], i[2])
                cv2.imshow('Output', img)
                cv2.waitKey(0)
            cv2.destroyAllWindows()
