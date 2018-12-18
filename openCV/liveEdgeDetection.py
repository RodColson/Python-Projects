#!/usr/bin/env python

'''
This sample demonstrates Canny edge detection.
Usage:
  edgeDetection.py [<video source>]
  Trackbars control edge thresholds.
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2 as cv
import numpy as np

# relative module
#import video

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

    cv.namedWindow('Edge Detection')

    cv.createTrackbar('T1', 'Edge Detection', 725, 5000, nothing)
    cv.createTrackbar('T2', 'Edge Detection', 725, 5000, nothing)
    
    cap = cv.VideoCapture(int(fn))
    while True:
        flag, img = cap.read()
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        T1 = cv.getTrackbarPos('T1', 'Edge Detection')
        T2 = cv.getTrackbarPos('T2', 'Edge Detection')
        edge = cv.Canny(gray, T1, T2, apertureSize=5, L2gradient=False)
        vis = img.copy()
        vis = np.uint8(vis/2.)
        vis[edge != 0] = (0, 255, 0)
        cv.putText(vis, "Press ESC to quit", (10, 15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv.imshow('Edge Detection', vis)
        ch = cv.waitKey(5)
        if ch == 27:
            break

    # do a bit of cleanup
    cap.release()
    cv.destroyAllWindows()
