'''
This sample demonstrates photo comparison.
Usage:
  imageCompare.py first-image second-image
'''

import argparse
import cv2
import numpy as np

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i1", "--input1", required=True, help="path to first input file")
ap.add_argument("-i2", "--input2", required=True, help="path to second input file")
args = vars(ap.parse_args())

# read images as 2D arrays (convert to grayscale for simplicity)
image1 = cv2.imread(args["input1"])
image2 = cv2.imread(args["input2"])
gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

# normalize to compensate for exposure difference
img1 = normalize(gray1)
img2 = normalize(gray2)

# resize to our desired dimensions for comparison
resized_img1 = cv2.resize(img1, (600, 600))
resized_img2 = cv2.resize(img2, (600, 600))
cv2.imshow("Input Photo 1", cv2.resize(image1, (0,0), fx=0.25, fy=0.25))
cv2.imshow("Input Photo 2", cv2.resize(image2, (0,0), fx=0.25, fy=0.25))
cv2.imshow("Normalized Photo 1", cv2.resize(img1, (0,0), fx=0.25, fy=0.25))
cv2.imshow("Normalized Photo 2", cv2.resize(img2, (0,0), fx=0.25, fy=0.25))
cv2.imshow("Resized Photo 1", resized_img1)
cv2.imshow("Resized Photo 2", resized_img2)

# compute difference percentage
#dif = np.sum(np.abs(resized_img1-resized_img2))
dif = np.sum(np.abs(img1-img2))
size = 1
for dim in np.shape(img1):
    size *= dim
pct = 1 - (dif/size)

print("Percentage similarity: {}".format(pct))

# wait for ESC key
while True:
    key = cv2.waitKey()

    # if the ESC key was pressed, break from the loop
    if key == 27:
        break
cv2.destroyAllWindows()
