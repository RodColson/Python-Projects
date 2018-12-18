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
cv2.imshow("Input Photo", image)

# Convert image to LAB Color model (L = Lightness, A = Green-Red, B = Blue-Yellow)
lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
cv2.imshow("LAB Color Model", lab)

# Split the LAB image to different channels
l, a, b = cv2.split(lab)
cv2.imshow('L Channel', l)
cv2.imshow('A Channel', a)
cv2.imshow('B Channel', b)

# Apply CLAHE to L-channel (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
cl = clahe.apply(l)
cv2.imshow('CLAHE Output', cl)

# Merge the CLAHE enhanced L-channel with the a and b channel
limg = cv2.merge((cl, a, b))
cv2.imshow('L Image', limg)

# Convert image from LAB Color model to RGB model
final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

cv2.imshow("Output Photo", final)

# High contrast method
imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
imghsv[:,:,2] = [[max(pixel - 25, 0) if pixel < 190 else min(pixel + 25, 255) for pixel in row] for row in imghsv[:,:,2]]
cv2.imshow('High Contrast', cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR))

cv2.waitKey(0)
cv2.destroyAllWindows()
