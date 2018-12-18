# import the necessary packages
import argparse
import cv2
import imutils
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,	help="path to input file")
args = vars(ap.parse_args())

image = cv2.imread(args["input"])
image = imutils.resize(image, width=640)
cv2.putText(image, "Press ESC to quit", (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (64,64,64), 2)
cv2.imshow("Input Photo", image)

# Contour detection
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
_, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

# Draw rectangles
for cnt in contours:
    if cv2.contourArea(cnt)>150:
        [x,y,w,h] = cv2.boundingRect(cnt)

        if  w>540:
            cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            cv2.imshow('Object Rectangles',image)

while True:
	key = cv2.waitKey(0)

	# if the ESC key was pressed, break from the loop
	if key == 27:
		break
cv2.destroyAllWindows()
