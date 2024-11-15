# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries for the given colour
# ball in the HSV color space

#multiple_balls
Lower = (29, 86, 6)
Upper = (64, 255, 255)
"""
#single_ball
Lower = (90, 50, 50)
Upper = (130, 255, 255)
"""
# initialize the list of tracked points, the frame counter,
# and the coordinate deltas
pts = deque(maxlen=args["buffer"])
counter = 0
(dX, dY) = (0, 0)
(d2X, d2Y) = (0, 0)
(dXnew, dYnew) = (0, 0)
direction = ""

if True :
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color given, then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, Lower, Upper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	
    	# only proceed if at least one contour was found
	if len(cnts) > 0:
	
		for c in cnts:	
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			# only proceed if the radius meets a minimum size
			if radius > 10:
				# draw the circle and centroid on the frame,
				# then update the list of tracked points
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				pts.appendleft(center)
			


	# loop over the set of tracked points
	for i in np.arange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# check to see if enough points have been accumulated in
		# the buffer
		if counter >= 10 and i == 1 and pts[-10] is not None:
			# compute the difference between the x and y
			# coordinates and re-initialize the direction
			# text variables
			#buffer frame is 32
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			dXnew = pts[-5][0] - pts[i][0]
			dYnew = pts[-5][1] - pts[i][1]
			d2X = dX - dXnew
			d2Y = dY - dYnew
			

			
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
 	
#		thickness = 2
#		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

		if center is not None:
			arrow_length = 3
			arrow_endpoint = (center[0] - arrow_length * dX, center[1] - arrow_length * dY)
			cv2.arrowedLine(frame, center, arrow_endpoint, (0, 255, 0), 2)
        	
		
	cv2.putText(frame, "d2x: {}, d2y: {}".format(d2X, d2Y),
		(10, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	cv2.putText(frame, "dx1: {}, dy1: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
vs.release()
# close all windows
cv2.destroyAllWindows()
