from tagInfo import *
# from picamera import PiCamera
from PIL import Image
import time
# import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help = "path to the (optional) video file")
args = vars(ap.parse_args())

camera = cv2.VideoCapture(args["video"])
while 1:
	(grabbed, frame) = camera.read()
	if not grabbed:
		break
	cv2.imwrite("mysample.jpg", frame)
	im = Image.open("mysample.jpg")
	im.save("mysample.ppm")
	val = tagInfo('mysample.ppm')
	print val





# with PiCamera() as camera:
# 	camera.resolution = (640, 480)
# 	while 1:
# 		camera.capture('foo.jpg')
# 		im = Image.open(name+".jpg")
# 		# im.rotate(90).show()
# 		im.rotate(180).save(name+"_2.ppm")

# val = tagInfo('sample.ppm')

# print val

