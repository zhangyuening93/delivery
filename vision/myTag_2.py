from tagInfo import *
from picamera import PiCamera
from PIL import Image
from PIL import ImageEnhance as IE
import time
# import numpy as np
import argparse
# import cv2

# camera = cv2.VideoCapture(args["video"])
with PiCamera() as camera:
	camera.resolution = (640, 480)
	while 1:
		mytime = time.time()
		camera.capture('mysample.jpg')
		mytime = time.time() - mytime
		print mytime
		mytime = time.time()
		im = Image.open("mysample.jpg")
		enh = IE.Color(im)
		im_2 = enh.enhance(0)
		wb = IE.Contrast(im_2)
		im_3 = wb.enhance(4)
		im_3.save("mysample.ppm")
		mytime = time.time() - mytime
		print mytime
		mytime = time.time()
		val = tagInfo('mysample.ppm')
		print val
		mytime = time.time() - mytime
		print mytime



