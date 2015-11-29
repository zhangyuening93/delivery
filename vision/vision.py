from tagInfo import *
from PIL import Image
from picamera import Picamera
import time

# Define
DEBUG = 1

def decodeLoc(value):
    # return (row, col)
    return math.floor(value/NUMCOL), value%NUMCOL

class TagCamera(object):
	def __init__(self):
		self._camera = Picamera()
		self._camera.resolution = (640, 480)

	def CaptureTag(self):
		self._camera.capture('mysample.jpg')
		im = Image.open('mysample.jpg')
		im.save('mysample.ppm')
		val = tagInfo('mysample.ppm')
		succeed = val[0]
		ID = val[1]
		width = val[2]
		height = val[3]
		angle = val[4]
		return succeed, ID, angle, (width, height)

	def getTagInfo():
	    # if fail to catch a tag, try 5 times
	    error_tolerance = 0
	    while 1:
	        detected, currentLoc, currentAngle, currentDis = self.CaptureTag()
	        if detected:
	            currentLoc = decodeLoc(currentLoc)
	            currentDis[0] = currentDis[0] - 320
	            currentDis[1] = currentDis[1] - 240
	            print "Location is: "+str(currentLoc)
	            print "Distance is: "+str(Tag.Distance)
	            print "Orientation is: "+str(currentAngle)
	            break
	        else:
	            print "No tag detected."
	            error_tolerance = error_tolerance + 1
	            if error_tolerance == 5:
	                # TODO: delete DEBUG
	                if DEBUG:
	                    getInput = raw_input("Which loc do you want to set? Press enter to continue.\n")
	                    if getInput == "":
	                        error_tolerance = 0
	                        time.sleep(0.2)
	                    else:
	                        currentLoc = getInput
	                        getInput = input("Which distance do you want to set?\n")
	                        currentDis= getInput
	                        getInput = input("Which orientation do you want to set?\n")
	                        currentAngle = getInput
	                        print "Location is: "+str(currentLoc)
	                        print "Distance is: "+str(Tag.Distance)
	                        print "Orientation is: "+str(currentAngle)
	                        break
	                else:
	                    return detected, 0, 0, (0, 0)
	            else:
	                time.sleep(0.2)
	    return detected, currentLoc, currentAngle, currentDis