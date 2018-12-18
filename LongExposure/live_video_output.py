# import the necessary packages
#from imutils.video import VideoStream
from imutils.video import FPS
import time
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", required=True,
#	help="path to input video file")
#ap.add_argument("-o", "--output", required=True,
#	help="path to output 'long exposure'")
#args = vars(ap.parse_args())

# initialize the Red, Green, and Blue channel averages, along with
# the total number of frames read from the file
(rAvg, gAvg, bAvg) = (None, None, None)
total = 0
 
# open a pointer to the video file
print("[INFO] opening video file pointer...")
stream = cv2.VideoCapture(0)

# wait 2 seconds for the camera to warm up
time.sleep(2.0)
fps = FPS().start()

# get the width and height in order to position the windows
width = stream.get(3)
height = stream.get(4)
print("[INFO] Width: {}".format(width))
print("[INFO] Height: {}".format(height))

# setup the windows
cv2.namedWindow("Live Video")
cv2.moveWindow("Live Video", 10, 10)
cv2.namedWindow("Averaged Video")
cv2.moveWindow("Averaged Video", int(width) + 10, 10)

# loop over frames from the video stream
while True:
	# grab the frame from the stream
	(grabbed, frame) = stream.read()
 
	# if the frame was not grabbed, then break out
	if not grabbed:
		break

	# show the grabbed frame
	cv2.imshow("Live Video", frame)

	key = cv2.waitKey(1) & 0xFF

	# if the `ESC` key was pressed, break from the loop
	if key == 27:
		break

	# update the FPS counter
	fps.update()
 
	# otherwise, split the frmae into its respective channels
	(B, G, R) = cv2.split(frame.astype("float"))
	
	# if the frame averages are None, initialize them
	if rAvg is None:
		rAvg = R
		bAvg = B
		gAvg = G
 
	# otherwise, compute the weighted average between the history of
	# frames and the current frames
	else:
		rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
		gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
		bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)
 
	# increment the total number of frames read thus far
	total += 1

	# merge the RGB averages together
	avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")

	# show the averaged frame
	cv2.imshow("Averaged Video", avg)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()
