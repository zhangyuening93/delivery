# from tagInfo import *
# from PIL import Image
# from picamera import Picamera
import time
import math


# Define
DEBUG = 1
NUMCOL = 10


def decodeLoc(value):
    # return (row, col)
    return (int(math.floor(value/NUMCOL)), int(value%NUMCOL))

class TagCamera(object):
    def __init__(self):
        pass


    def getTagInfo(self):
        # if fail to catch a tag, try 5 times
        currentLoc = input("Which loc do you want to set?\n")
        currentDis = input("Which distance do you want to set?\n")
        currentAngle = input("Which orientation do you want to set?\n")
        print "Location is: "+str(currentLoc)
        print "Distance is: "+str(currentDis)
        print "Orientation is: "+str(currentAngle)
        return 1, currentLoc, currentAngle, currentDis
