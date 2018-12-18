'''
This sample demonstrates object recognition.
Usage:
  liveObjectRecognition.py --size matrixSize
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
ap.add_argument("-s", "--size", type=int, required=True, help="size of comparison matrix")
ap.add_argument("-t", "--threshold", type=float, default=0.8, help="minimum similarity to filter weak detections")
args = vars(ap.parse_args())

# define the location of the reference photos to compare against 
refdir = './MANTA/ImageCapture/'
arrayImage = []
arrayRef = []
arrayFiles = []

# iterate through the photos in the reference folder and build a comparison array
for root, dirs, filenames in os.walk(refdir):
    filenames = [ fi for fi in filenames if fi.endswith(".jpg") ]
    for f in filenames:
        refImage = cv2.imread(refdir + f)
        refGray = cv2.cvtColor(refImage, cv2.COLOR_BGR2GRAY)
        refNorm = normalize(refGray)
        refResized = cv2.resize(refNorm, (args["size"], args["size"]))
        arrayImage.append(refImage)
        arrayRef.append(refResized)
        arrayFiles.append(f)

# create a nomatch image
noMatch = np.zeros(refImage.shape)

# set up video capture
cap = cv2.VideoCapture(0)

# read a frame from video capture device (convert to grayscale for simplicity)
while True:
    flag, inputFrame = cap.read()
    cv2.imshow("INPUT", cv2.resize(inputFrame, (0,0), fx=0.5, fy=0.5))
    inputGray = cv2.cvtColor(inputFrame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("INPUT GRAY", cv2.resize(inputGray, (0,0), fx=0.5, fy=0.5))

    # normalize to compensate for exposure difference
    inputNorm = normalize(inputGray)
    #cv2.imshow("INPUT NORMALIZED", cv2.resize(inputNorm, (0,0), fx=0.5, fy=0.5))

    # resize to our desired dimensions for comparison
    inputResized = cv2.resize(inputNorm, (args["size"], args["size"]))

    # iterate through the reference array comparing aganst the input frame
    bestPct = 0
    arrayRef = np.array(arrayRef)
    for seq in range (0, arrayRef.shape[0]):
        # compute difference percentage
        dif = np.sum(np.abs(inputResized-arrayRef[seq]))
        pct = 1 - (dif/(args["size"]*args["size"]))
        print("Dif: {}".format(dif))
        print("Pct: {}".format(pct))
        
        if pct > bestPct:
            bestPct = pct
            bestSeq = seq
            bestFile = arrayFiles[seq]
            bestRefImage = arrayImage[seq]

    print("Best Pct: {}".format(bestPct))
    if bestPct < args["threshold"]:
        cv2.imshow("MATCH", cv2.resize(noMatch, (0,0), fx=0.5, fy=0.5))
    else:
        cv2.imshow("MATCH", cv2.resize(bestRefImage, (0,0), fx=0.5, fy=0.5))
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cv2.destroyAllWindows()
