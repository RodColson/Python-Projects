#!/usr/bin/env python

'''
This sample demonstrates HOG descriptors using SciKit
Usage:
  HOGDescriptor.py [<video source>]
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2 as cv
import numpy as np
from skimage.feature import hog

# built-in module
import sys

if __name__ == '__main__':
    print(__doc__)

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    def nothing(*arg):
        pass

    cap = cv.VideoCapture(int(fn))
    while True:
        flag, image = cap.read()
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        fd, hog_image = hog(gray, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), block_norm="L2-Hys", visualise=True, transform_sqrt=False)
        cv.putText(hog_image, "Press ESC to quit", (10, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv.imshow('HOG Descriptor', hog_image)
        
        ch = cv.waitKey(5)
        if ch == 27:
            break

    # do a bit of cleanup
    cap.release()
    cv.destroyAllWindows()

