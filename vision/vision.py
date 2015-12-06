from PIL import Image
from PIL import ImageEnhance as IE
from picamera import PiCamera
from tagInfo import *
import time
import math
import sys



# Define
# DEBUG = 1
NUMCOL = 5
CENTER_X = 320
CENTER_Y = 240
E_ANGLE = 270
N_ANGLE = 180
W_ANGLE = 90
S_ANGLE = 0


def getDirection(value):
    # return direction
    # if 1, then direction is correct, otherwise, correct direction
    # original value is -180~180
    value = value + 180
    if abs(value-E_ANGLE)<20:
        return 1, 'e'
    elif abs(value-N_ANGLE)<20:
        return 1, 'n'
    elif abs(value-S_ANGLE)<20 or abs(value-S_ANGLE)>340:
        return 1, 's'
    elif abs(value-W_ANGLE)<20:
        return 1, 'w'
    else:
        return 0, 'b'

# def updateLoc(currentLoc, currDir, offset):
#     if currDir == 's':
#         newLoc = (currentLoc[0] + offset, currentLoc[1])
#     elif currDir == 'e':
#         newLoc = (currentLoc[0], currentLoc[1] + offset)
#     elif currDir == 'w':
#         newLoc = (currentLoc[0], currentLoc[1] - offset)
#     elif currDir == 'n':
#         newLoc = (currentLoc[0] - offset, currentLoc[1])
#     return newLoc

def getLRCommand(currDir, goalDir):
    if currDir == 's':
        if goalDir == 'e':
            return 'L'
        else:
            return 'R'
    if currDir == 'n':
        if goalDir == 'w':
            return 'L'
        else:
            return 'R'
    if currDir == 'w':
        if goalDir == 's':
            return 'L'
        else:
            return 'R'
    if currDir == 'e':
        if goalDir == 'n':
            return 'L'
        else:
            return 'R'   
    print "error[1]"
    sys.exit(1)


def decodeLoc(value):
    # return (row, col)
    return (int(math.floor(value/NUMCOL)), int(value%NUMCOL))

def readNextCommand(path, currentLoc, currentAngle, currentDis):
    # return the next command and the next location
    # At first, idx = 0
    suc, currDir = getDirection(currentAngle)
    # TODO: Need to check distance.
    if suc:
        if path != "" and path[0] == currDir:
            print "current direction is: "+currDir+". Direction matches."
            # case: Forward
            return 'A' # A is going forward
        else:
            print "current direction is: "+currDir+". Direction does not match."
            # case: small forward
            if currentDis[1] < -15:
                command = 'B' # B is going forward a bit
            elif currentDis[1] > 15:
                command = 'C' # C is going backwards a bit
            elif path!="":
            # case: turning
                command = getLRCommand(currDir, path[0])
            else:
                command = 'S'
            return command
    else:
        # TODO: Need commands for minor adjustments
        print "error[2]"
        sys.exit(1)

class TagCamera(object):
    def __init__(self):
        self._camera = PiCamera()
        self._camera.resolution = (640, 480)

    def CaptureTag(self):
        self._camera.capture('mysample.jpg')
        im = Image.open('mysample.jpg')
        enh = IE.Color(im)
        im_2 = enh.enhance(0)
        im_2.save('mysample.ppm')
        val = tagInfo('mysample.ppm')
        succeed = val[0]
        ID = val[1]
        width = val[2]
        height = val[3]
        angle = val[4]
        if not succeed:
            wb = IE.Contrast(im_2)
            im_3 = wb.enhance(9)
            im_3.save('mysample1.ppm')
            val = tagInfo('mysample1.ppm')
            succeed = val[0]
            ID = val[1]
            width = val[2]
            height = val[3]
            angle = val[4]
        return succeed, ID, angle, (width, height)

    def getTagInfo(self):
        # if fail to catch a tag, try 5 times
        # error_tolerance = 0
        # while 1:
        detected, currentLoc, currentAngle, currentDis = self.CaptureTag()
        if detected:
            currentLoc = decodeLoc(currentLoc)
            currentDis = (currentDis[0] - CENTER_X,currentDis[1] - CENTER_Y)
            print "Location is: "+str(currentLoc)
            print "Distance is: "+str(currentDis)
            print "Orientation is: "+str(currentAngle)
            # break
        else:
            print "No tag detected."
            return detected, 0, 0, (0, 0)
                # error_tolerance = error_tolerance + 1
                # if error_tolerance == 5:
                #     # TODO: delete DEBUG
                #     if DEBUG:
                #         getInput = raw_input("Do you want to keep trying? y/enter\n")
                #         if getInput == "":
                #             error_tolerance = 0
                #             time.sleep(0.2)
                #         elif getInput == 'y':
                #             currentLoc = input("Which loc do you want to set?\n")
                #             currentDis = input("Which distance do you want to set?\n")
                #             currentAngle = input("Which orientation do you want to set?\n")
                #             detected = 1
                #             print "Location is: "+str(currentLoc)
                #             print "Distance is: "+str(currentDis)
                #             print "Orientation is: "+str(currentAngle)
                #             break
                #         else:
                #             return detected, 0, 0, (0, 0)
                #     else:
                # else:
                #     time.sleep(0.2)
        return detected, currentLoc, currentAngle, currentDis


# class TagCamera(object):
#     def __init__(self):
#         pass


#     def getTagInfo(self):
#         # if fail to catch a tag, try 5 times
#         currentLoc = input("Which loc do you want to set?\n")
#         currentDis = input("Which distance do you want to set?\n")
#         currentAngle = input("Which orientation do you want to set?\n")
#         print "Location is: "+str(currentLoc)
#         print "Distance is: "+str(currentDis)
#         print "Orientation is: "+str(currentAngle)
#         return 1, currentLoc, currentAngle, currentDis
