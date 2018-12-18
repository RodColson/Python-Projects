# import the necessary packages
#from imutils.video import VideoStream
from imutils.video import FPS
import time
import argparse
import imutils
import cv2
import numpy as np
 
# open a pointer to the video file
print("[INFO] opening video stream...")
stream = cv2.VideoCapture(0)

# wait 2 seconds for the camera to warm up
time.sleep(2.0)
fps = FPS().start()

# initialize averaged frame
(grabbed,frame) = stream.read()
avgframe = np.float32(frame)

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

	# if the `q` key was pressed, break from the loop
	if key == 27:
		break

	# update the FPS counter
	fps.update()

 	# accumulate logic
 	# the alpha parameter (float 0-1) controls how fast the accumulator forgets earlier frames (lower = longer memory)
	cv2.accumulateWeighted(frame, avgframe, 0.02)
	avgframeres = cv2.convertScaleAbs(avgframe)

	# show the averaged frame
	cv2.imshow("Averaged Video", avgframeres)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()
cv2.destroyAllWindows()
