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
    scale = 255/rng
    return (arr-amin)*scale

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s", "--size", type=int, required=True, help="size of comparison matrix")
ap.add_argument("-t", "--threshold", type=float, default=0.8, help="minimum similarity to filter weak detections")
args = vars(ap.parse_args())

# define the location of the reference photos to compare against 
refdir = './MANTA/ImageCapture/'
arrayImage = []
arrayRefBlue = []
arrayRefGreen = []
arrayRefRed = []
arrayFiles = []

# iterate through the photos in the reference folder and build a comparison array
for root, dirs, filenames in os.walk(refdir):
    filenames = [ fi for fi in filenames if fi.endswith(".jpg") ]
    for f in filenames:
        refImage = cv2.imread(refdir + f)
        refResized = cv2.resize(refImage, (args["size"], args["size"]))
        b,g,r = cv2.split(refResized)
        arrayImage.append(refImage)
        normalizedBlue = normalize(b)
        normalizedGreen = normalize(g)
        normalizedRed = normalize(r)
        arrayRefBlue.append(normalizedBlue)
        arrayRefGreen.append(normalizedGreen)
        arrayRefRed.append(normalizedRed)
        arrayFiles.append(f)

# create a nomatch image
noMatch = np.zeros(refImage.shape)

arrayRefBlue = np.array(arrayRefBlue)
arrayRefGreen = np.array(arrayRefGreen)
arrayRefRed = np.array(arrayRefRed)

# set up video capture
cap = cv2.VideoCapture(0)

# read a frame from video capture device
while True:
    flag, inputFrame = cap.read()
    cv2.imshow("INPUT", cv2.resize(inputFrame, (0,0), fx=0.5, fy=0.5))

    # resize to our desired dimensions for comparison
    inputResized = cv2.resize(inputFrame, (args["size"], args["size"]))

    b,g,r = cv2.split(inputResized)
    inputBlue = normalize(b)
    inputGreen = normalize(g)
    inputRed = normalize(r)
    
    cv2.imshow("INPUT BLUE", cv2.resize(b, (0,0), fx=4, fy=4))
    cv2.imshow("INPUT GREEN", cv2.resize(g, (0,0), fx=4, fy=4))
    cv2.imshow("INPUT RED", cv2.resize(r, (0,0), fx=4, fy=4))
    
    # iterate through the reference array comparing aganst the input frame
    bestPct = 0
    for seq in range (0, arrayRefBlue.shape[0]):
        # compute difference percentage
        difBlue = np.sum(np.abs(inputBlue-arrayRefBlue[seq]))
        difGreen = np.sum(np.abs(inputGreen-arrayRefGreen[seq]))
        difRed = np.sum(np.abs(inputRed-arrayRefRed[seq]))
        pctBlue = 1 - (difBlue/(args["size"]*args["size"])/255)
        pctGreen = 1 - (difGreen/(args["size"]*args["size"])/255)
        pctRed = 1 - (difRed/(args["size"]*args["size"])/255)
        if (pctBlue + pctGreen + pctRed) / 3 > bestPct:
            bestPct = (pctBlue + pctGreen + pctRed) / 3
            bestSeq = seq
            bestFile = arrayFiles[seq]
            bestRefImage = arrayImage[seq]

    print("Best Pct: {}".format(bestPct))
    if bestPct < args["threshold"]:
        cv2.imshow("MATCH", cv2.resize(noMatch, (0,0), fx=0.5, fy=0.5))
    else:
        cv2.imshow("MATCH", cv2.resize(bestRefImage, (0,0), fx=0.5, fy=0.5))
        cv2.putText(inputFrame,bestFile,(20,30), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("INPUT", cv2.resize(inputFrame, (0,0), fx=0.5, fy=0.5))
    ch = cv2.waitKey(5)
    if ch == 27:
        break

cv2.destroyAllWindows()
