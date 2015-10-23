# USAGE
# python track.py --video video/iphonecase.mov

# import the necessary packages
import numpy as np
import argparse
import time
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

# define the upper and lower boundaries for a color
# to be considered "blue"
blueLower = np.array([0, 0, 0], dtype = "uint8")
blueUpper = np.array([50, 50, 50], dtype = "uint8")
orientation_flag = [[1,1,0,0],
					[0,1,1,0],
					[0,0,1,1],
					[1,0,0,1]]

# load the video
camera = cv2.VideoCapture(args["video"])
(grabbed, frame) = camera.read()
car_center = (frame.shape[0]/2,frame.shape[1]/2)
# print video_center

# keep looping
while True:
	# grab the current frame
	(grabbed, frame) = camera.read()

	# check to see if we have reached the end of the
	# video
	if not grabbed:
		break

	# determine which pixels fall within the blue boundaries
	# and then blur the binary image
	blue = cv2.inRange(frame, blueLower, blueUpper)
	blue = cv2.GaussianBlur(blue, (3, 3), 0)

	# find contours in the image
	(cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# check to see if any contours were found
	if len(cnts) > 0:
		# sort the contours and find the largest one -- we
		# will assume this contour correspondes to the area
		# of my phone
		cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

		# compute the (rotated) bounding box around then
		rect = np.int32(cv2.cv.BoxPoints(cv2.minAreaRect(cnt)))
		rect_t = np.transpose(rect)
		# compute distance
		bar_center = (int(np.mean(rect_t[0])),int(np.mean(rect_t[1])))
		# print bar_center
		distance = (bar_center[0]-car_center[0],bar_center[1]-car_center[1])
		cv2.circle(frame, bar_center, 5, (255, 0, 0), -1)
		# print distance
		# print rect
		# compute original orientation of the car
		angle = np.arctan2(rect[2][0]-rect[1][0],rect[2][1]-rect[1][1])*180/np.pi
		# contour and then draw it		
		cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)
		pts = np.float32([[100,100],[0,100],[0,0],[100,0]])
		M = cv2.getPerspectiveTransform(np.float32(rect),pts)
		p_image = cv2.warpPerspective(frame,M,(100,100))
		gray = cv2.cvtColor(p_image, cv2.COLOR_BGR2GRAY)
		# cv2.circle(frame, (rect[0][0],rect[0][1]), 5, (0, 255, 0), -1)
		# cv2.circle(frame, (rect[1][0],rect[1][1]), 5, (255, 0, 0), -1)
		# cv2.circle(frame, (rect[2][0],rect[2][1]), 5, (0, 0, 255), -1)
		# cv2.circle(frame, (rect[3][0],rect[3][1]), 5, (255, 255, 0), -1)
		(T, threshInv) = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)
		rs_image = cv2.resize(threshInv, (8, 8), interpolation = cv2.INTER_AREA)
		(T, thresh) = cv2.threshold(rs_image, 155, 1, cv2.THRESH_BINARY)
		point_value = [thresh[1][1],thresh[1][6],thresh[6][6],thresh[6][1]]
		# print angle
		if point_value == orientation_flag[0]:
			pass
		elif point_value == orientation_flag[1]:
			thresh = cv2.transpose(thresh)
			thresh = cv2.flip(thresh,flipCode = 0)
			threshInv = cv2.transpose(threshInv)
			threshInv = cv2.flip(threshInv,flipCode = 0)
			angle = angle - 90
		elif point_value == orientation_flag[2]:
			thresh = cv2.transpose(thresh)
			thresh = cv2.flip(thresh,flipCode = 0)
			thresh = cv2.transpose(thresh)
			thresh = cv2.flip(thresh,flipCode = 0)
			threshInv = cv2.transpose(threshInv)
			threshInv = cv2.flip(threshInv,flipCode = 0)
			threshInv = cv2.transpose(threshInv)
			threshInv = cv2.flip(threshInv,flipCode = 0)
			angle = angle
		elif point_value == orientation_flag[3]:
			thresh = cv2.transpose(thresh)
			thresh = cv2.flip(thresh,flipCode = 1)
			threshInv = cv2.transpose(threshInv)
			threshInv = cv2.flip(threshInv,flipCode = 1)
			angle = angle + 90
		print angle

	# show the frame and the binary image
	# print thresh
	value = 0
	for x in xrange(6):
		value = value*2 + thresh[1][x+1]
	# print value
	# cv2.imshow("threshold",threshInv)
	cv2.imshow("Tracking", frame)
	#cv2.imshow("Binary", blue)
	# cv2.imshow("Cropped",p_image)
	# cv2.waitKey(0)

	# if your machine is fast, it may display the frames in
	# what appears to be 'fast forward' since more than 32
	# frames per second are being displayed -- a simple hack
	# is just to sleep for a tiny bit in between frames;
	# however, if your computer is slow, you probably want to
	# comment out this line
	#time.sleep(0.025)

	# if the 'q' key is pressed, stop the loop
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()