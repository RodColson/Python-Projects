'''
This sample demonstrates object recognition.
Usage:
  objectRecognition.py --image imagefile --size vectorsize
'''

import argparse
import cv2
import numpy as np
import os

def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image file")
ap.add_argument("-s", "--size", required=True, help="size of comparison vectors")
args = vars(ap.parse_args())

# read image as 2D arrays (convert to grayscale for simplicity)
inputImage = cv2.imread(args["image"])
inputGray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

# normalize to compensate for exposure difference
inputNorm = normalize(inputGray)

# resize to our desired dimensions for comparison
size = int(args["size"])
inputResized = cv2.resize(inputNorm, (size, size))

# display the input image
cv2.imshow("Input Photo", cv2.resize(inputImage, (0,0), fx=0.1, fy=0.1))

# define the location of the reference photos to compare against
refdir = './MANTA/ReferencePhotos/'
bestPct = 0

# iterate through the photos in the reference folder comparing aganst the input photo
for root, dirs, filenames in os.walk(refdir):
    for f in filenames:
        refImage = cv2.imread(refdir + f)
        refGray = cv2.cvtColor(refImage, cv2.COLOR_BGR2GRAY)
        refNorm = normalize(refGray)
        refResized = cv2.resize(refNorm, (size, size))
        
        # compute difference percentage
        dif = np.sum(np.abs(inputResized-refResized))
        pct = 1 - (dif/(size*size))
        if pct > bestPct:
            bestPct = pct
            bestRefImage = refImage
            bestF = f
        # display each reference photo
        cv2.imshow(f, cv2.resize(refImage, (0,0), fx=0.1, fy=0.1))
        print("Filename: {}  Similarity: {}".format(f, pct))

# display the best matched photo
cv2.putText(bestRefImage, bestF, (150, 250), cv2.FONT_HERSHEY_SIMPLEX, 8, (0,255,0), 10)
cv2.imshow("MATCH", cv2.resize(bestRefImage, (0,0), fx=0.1, fy=0.1))

# wait for ESC key
while True:
    key = cv2.waitKey()

    # if the ESC key was pressed, break from the loop
    if key == 27:
        break
cv2.destroyAllWindows()
