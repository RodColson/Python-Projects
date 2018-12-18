'''
This is a utility to capture images from the webcam
'''

import cv2
import numpy as np

# define the location of the reference photos to compare against and the size of our comparison vector
refdir = './MANTA/ImageCapture/'

# set up video capture
cap = cv2.VideoCapture(0)

# create a nomatch image
flag, inputFrame = cap.read()

# read a frame from video capture device (convert to grayscale for simplicity)
num = 0
while True:
    flag, inputFrame = cap.read()
    cv2.imshow('Image', inputFrame)

    ch = cv2.waitKey(5)
    if ch == 32:
        num = num + 1
        cv2.imwrite(refdir + 'image' + format(num) + '.jpg', inputFrame)

    if ch == 27:        
        break

cv2.destroyAllWindows()
