'''
This sample demonstrates object recognition.
Usage:
  liveObjectRecognition.py --size matrixSize
'''

import cv2 as cv
import numpy as np
from scipy.spatial import distance

# set up video capture
cap = cv.VideoCapture(0)

dst = np.float32([(0, 0),
                  (640, 0),
                  (640, 480),
                  (0, 480)])

def sortpts_clockwise(A):
    # Sort A based on Y(col-2) coordinates
    sortedAc2 = A[np.argsort(A[:,1]),:]

    # Get top two and bottom two points
    top2 = sortedAc2[0:2,:]
    bottom2 = sortedAc2[2:,:]

    # Sort top2 points to have the first row as the top-left one
    sortedtop2c1 = top2[np.argsort(top2[:,0]),:]
    top_left = sortedtop2c1[0,:]

    # Use top left point as pivot & calculate sq-euclidean dist against
    # bottom2 points & thus get bottom-right, bottom-left sequentially
    sqdists = distance.cdist(top_left[None], bottom2, 'sqeuclidean')
    rest2 = bottom2[np.argsort(np.max(sqdists,0))[::-1],:]

    # Concatenate all these points for the final output
    return np.concatenate((sortedtop2c1,rest2),axis =0)
                  
# read a frame from video capture device (convert to grayscale for simplicity)
while True:
    flag, img = cap.read()
    #cv.imshow('image', img)
    h, w = img.shape[:2]

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    
    corners = cv.goodFeaturesToTrack(gray, 4, 0.005, 200)
    corners = np.int0(corners)
    
    src = []
    cnt = 0
    for i in corners:
        cnt = cnt + 1
        x, y = i.ravel()
        src.append([x, y])
        cv.circle(img, (x, y), 3, (0, 0, 255), -1)
    
    cv.imshow('corners', img)
    
    # only unwarp the image if we found 4 corners
    if cnt == 4:
        src = np.float32(src)
        src = sortpts_clockwise(src)
                     
        # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
        M = cv.getPerspectiveTransform(src, dst)
        # use cv2.warpPerspective() to warp your image to a top-down view
        warped = cv.warpPerspective(img, M, (w, h), flags=cv.INTER_LINEAR)

        cv.imshow("Corrected", cv.resize(warped, (0,0), fx=1, fy=1))
    
    ch = cv.waitKey(5)
    if ch == 27:
        break
    
cv.destroyAllWindows()
