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
h, w = image.shape[:2]

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
_, contours0, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

def update(levels):
	vis = np.zeros((h, w, 3), np.uint8)
	levels = levels - 3
	cv2.drawContours(vis, contours, levels, (128,255,255), 2, cv2.LINE_AA, hierarchy, abs(levels))
	cv2.imshow("Contours", vis)

update(1)
cv2.createTrackbar("Hierarchy Level", "Contours", 1, 3, update)

while True:
	key = cv2.waitKey()

	# if the ESC key was pressed, break from the loop
	if key == 27:
		break
cv2.destroyAllWindows()
