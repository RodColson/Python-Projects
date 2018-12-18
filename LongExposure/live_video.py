# import the necessary packages
#from imutils.video import VideoStream
from imutils.video import FPS
import time
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
#ap.add_argument("-v", "--video", required=True,
#	help="path to input video file")
ap.add_argument("-o", "--output", required=True,
	help="path to output 'long exposure'")
args = vars(ap.parse_args())

# initialize the Red, Green, and Blue channel averages, along with
# the total number of frames read from the file
(rAvg, gAvg, bAvg) = (None, None, None)
total = 0
 
# open a pointer to the video file
print("[INFO] opening video file pointer...")
stream = cv2.VideoCapture(1)

time.sleep(2.0)
fps = FPS().start()

print("[INFO] computing frame averages (this will take awhile)...")
# loop over frames from the video file stream
while True:
	# grab the frame from the file stream
	(grabbed, frame) = stream.read()
 
	# if the frame was not grabbed, then we have reached the end of
	# the sfile
	if not grabbed:
		break

 	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
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

# merge the RGB averages together and write the output image to disk
avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")

cv2.imwrite(args["output"], avg)

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
stream.release()

# load and display the final image
image = cv2.imread(args["output"])
cv2.imshow("Long Exposure", imutils.resize(image, width=600))
cv2.waitKey(0)

# final cleanup
cv2.destroyAllWindows()
