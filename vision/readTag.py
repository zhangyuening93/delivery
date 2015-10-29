# import the necessary packages
from picamera import PiCamera
from picamera.array import PiRGBArray
import numpy as np
import time
import cv2

######################################################
# Usage:
# Tag = TagInfo()
# Tag.Capture()
# if Tag.TagDetected:
# 	read Tag.Distance, Tag.Orientation, Tag.Value
######################################################

class TagInfo(object):
	def __init__(self):
		# define macros
		self._blueLower = np.array([0, 0, 0], dtype = "uint8")
		self._blueUpper = np.array([60, 60, 60], dtype = "uint8")
		self._orientation_flag = [[1,1,0,0],
								[0,1,1,0],
								[0,0,1,1],
								[1,0,0,1]]
		self._car_center = (640/2,480/2)
		self._error_check_value_1 = 39
		self._error_check_value_2 = 18
		self._threshold_value = 60

		# define variables
		self.TagDetected = 0
		self.Distance = (0,0)
		self.Orientation = 0
		self.Value = 0

		# initialize camera
		self._camera = PiCamera()
		self._camera.resolution = (640, 480)
		self._camera.framerate = 32
		self._rawCapture = PiRGBArray(self._camera,size = (640,480))

		# warm up camera
		time.sleep(0.1)

	def StreamVideo(self):
		# capture frames from stream
		for image_raw in self._camera.capture_continuous(self._rawCapture, format="bgr",use_video_port=True):
			frame = image_raw.array
			# cv2.imshow("Frame",frame)
			self.process(frame)
			self._rawCapture.truncate(0)
			# if the 'q' key is pressed, stop the loop
			if cv2.waitKey(1) & 0xFF == ord("q"):
				break

	def Capture(self):
		# capure frame once
		self._camera.capture(self._rawCapture, format="bgr")
		frame = self._rawCapture.array
		self.process(frame)
		self._rawCapture.truncate(0)

	def process(self, frame):
		# determine which pixels fall within the blue boundaries
		# and then blur the binary image
		blue = cv2.inRange(frame, self._blueLower, self._blueUpper)
		blue = cv2.GaussianBlur(blue, (3, 3), 0)

		# find contours in the image
		(cnts, _) = cv2.findContours(blue.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)

		# check to see if any contours were found
		if len(cnts) > 0:
			# sort the contours and find the largest one
			cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

			# compute the (rotated) bounding box around then
			rect = np.int32(cv2.cv.BoxPoints(cv2.minAreaRect(cnt)))
			rect_t = np.transpose(rect)
			# compute distance
			bar_center = (int(np.mean(rect_t[0])),int(np.mean(rect_t[1])))
			# print bar_center
			distance = (bar_center[0]-self._car_center[0],bar_center[1]-self._car_center[1])
			cv2.circle(frame, bar_center, 5, (255, 0, 0), -1)
			# print distance
			# print rect
			# compute original orientation of the car
			angle = np.arctan2(rect[2][0]-rect[1][0],rect[2][1]-rect[1][1])*180/np.pi
			# contour and then draw it		
			cv2.drawContours(frame, [rect], -1, (0, 255, 0), 2)
			pts = np.float32([[100,100],[0,100],[0,0],[100,0]])
			# Perspective transform
			M = cv2.getPerspectiveTransform(np.float32(rect),pts)
			p_image = cv2.warpPerspective(frame,M,(100,100))
			# Gray image
			gray = cv2.cvtColor(p_image, cv2.COLOR_BGR2GRAY)
			# Take threshold
			(T, threshInv) = cv2.threshold(gray, self._threshold_value, 255, cv2.THRESH_BINARY)
			# Resize to 8*8
			rs_image = cv2.resize(threshInv, (8, 8), interpolation = cv2.INTER_AREA)
			# Take threshold
			(T, thresh) = cv2.threshold(rs_image, self._threshold_value, 1, cv2.THRESH_BINARY)
			point_value = [thresh[1][1],thresh[1][6],thresh[6][6],thresh[6][1]]
			# print angle
			if point_value == self._orientation_flag[0]:
				pass
			elif point_value == self._orientation_flag[1]:
				thresh = cv2.transpose(thresh)
				thresh = cv2.flip(thresh,flipCode = 0)
				threshInv = cv2.transpose(threshInv)
				threshInv = cv2.flip(threshInv,flipCode = 0)
				angle = angle - 90
			elif point_value == self._orientation_flag[2]:
				thresh = cv2.transpose(thresh)
				thresh = cv2.flip(thresh,flipCode = 0)
				thresh = cv2.transpose(thresh)
				thresh = cv2.flip(thresh,flipCode = 0)
				threshInv = cv2.transpose(threshInv)
				threshInv = cv2.flip(threshInv,flipCode = 0)
				threshInv = cv2.transpose(threshInv)
				threshInv = cv2.flip(threshInv,flipCode = 0)
				angle = angle + 180
			elif point_value == self._orientation_flag[3]:
				thresh = cv2.transpose(thresh)
				thresh = cv2.flip(thresh,flipCode = 1)
				threshInv = cv2.transpose(threshInv)
				threshInv = cv2.flip(threshInv,flipCode = 1)
				angle = angle + 90
			# print angle
			# Error check and read value
			value = 0
			value_2 = 0
			for x in xrange(6):
				value = value*2 + thresh[1][x+1]
				value_2 = value_2*2 + thresh[6][x+1]
			if value != self._error_check_value_1	or value_2 != self._error_check_value_2:
				print "Error."
				self.TagDetected = 0
			else:
				value = 0
				for x in xrange(6):
					value = value*2 + thresh[2][x+1]
				# print value
				self.TagDetected = 1
				self.Distance = distance
				self.Orientation = angle
				self.Value = value
			# print thresh
			# cv2.imshow("threshold",threshInv)
			# cv2.imshow("Binary", blue)
			# cv2.imshow("Cropped",p_image)

		# show the frame
		# cv2.imshow("Tracking", frame)
		# cv2.waitKey(0)
	
	
