from vision_2 import *
import socket
import time
# import serial
import sys
import errno
import exmod


# Define some parameters
BITS = 6
HOST = socket.gethostname()
E_ANGLE = 180
N_ANGLE = 270
W_ANGLE = 0
S_ANGLE = 90


def getDirection(value):
    # return direction
    # if 1, then direction is correct, otherwise, correct direction
    # original value is -180~180
    value = value + 180
    if abs(value-E_ANGLE)<10:
        return 1, 'e'
    elif abs(value-N_ANGLE)<10:
        return 1, 'n'
    elif abs(value-S_ANGLE)<10:
        return 1, 's'
    elif abs(value-W_ANGLE)<10 or abs(value-W_ANGLE)>350:
        return 1, 'w'
    else:
        return 0, 'b'

def updateLoc(currentLoc, currDir, offset):
    if currDir == 's':
        newLoc = (currentLoc[0] + offset, currentLoc[1])
    elif currDir == 'e':
        newLoc = (currentLoc[0], currentLoc[1] + offset)
    elif currDir == 'w':
        newLoc = (currentLoc[0], currentLoc[1] - offset)
    elif currDir == 'n':
        newLoc = (currentLoc[0] - offset, currentLoc[1])
    return newLoc

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


def readNextCommand(idx, path, currentLoc, currentAngle, currentDis):
    # return the next command and the next location
    # At first, idx = 0
    suc, currDir = getDirection(currentAngle)
    # TODO: Need to check distance.
    if suc:
        if path[idx] == currDir:
            print "current direction is: "+currDir+". Direction matches."
            # case: Forward
            offset = 1
            while 1:
                idx = idx + 1
                if idx < len(path):
                    if path[idx]==currDir:
                        offset = offset + 1
                    else:
                        newLoc = updateLoc(currentLoc, currDir, offset)
                        break
                else:
                    newLoc = updateLoc(currentLoc, currDir, offset)
                    break
            return idx, 'F'+str(offset), newLoc
        else:
            print "current direction is: "+currDir+". Direction does not match."
            # case: turning
            command = getLRCommand(currDir, path[idx])
            return idx, command+'90', currentLoc
    else:
        # TODO: Need commands for minor adjustments
        print "error[2]"
        sys.exit(1)


# Upon powering up, run main.py
print "Program starts."

# initialize socket, run server
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print "Server is on."

# Initialize uart
# usbport = '/dev/ttyAMA0'
# ser = serial.Serial(usbport, 9600)
# print "Uart established."

# Initialize camera
camera = TagCamera()
print "camera is on."

while 1:
    # Listen for requests
    s.listen(1)
    # Connect to a client
    conn, addr = s.accept()    
    print('Connected to', addr)
    # Receive the destination location from the client.
    destination = decodeLoc(int(conn.recv(1024)))
    print "Receive destination: "+str(destination)
    # Get the start location and orientation
    detected, currentLoc, currentAngle, currentDis = camera.getTagInfo()
    if not detected:
        print "I am lost at initial position."
        conn.send('F')
        print "Connection is dropped."
        conn.close()
        continue
    # Get the path
    # print currentLoc
    # print destination
    # print currentLoc[0]
    # print currentLoc[1]
    # print destination[0]
    # print destination[1]

    path = exmod.find_route(currentLoc[0], currentLoc[1], destination[0],destination[1])
    print path
    idx = 0
    # Start the main loop
    while 1:
        # Read the next target
        idx, command, target = readNextCommand(idx, path, currentLoc, currentAngle, currentDis)
        print "Next command is: "+command
        print "targetLoc is: "+str(target)
        # Send the command to MCU
        # ser.write(command)
        # ACK = ser.read() # TODO: Check if command is lost or incorrect
        # Receive the signal from MCU when reaching target
        # signal = ser.read()
        time.sleep(5)
        signal = 'f'
        # If MCU says if finishes
        # TODO: check if too long time without a signal
        if signal == 'f':
            # Sample a Tag to see if really finishes
            detected, currentLoc, currentAngle, currentDis = camera.getTagInfo()
            # Delete after
            if not detected:
                print "I am lost:(.."
                conn.send('F')
                print "Connection is dropped."
                conn.close()
                break
            if target!=currentLoc:
                print "I am lost:(.. I am now at "+str(currentLoc)
                conn.send('F')
                print "Connection is dropped."
                conn.close()
                break
            # Reaches target. Send position update to client
            sendLoc = currentLoc[0]*NUMCOL + currentLoc[1]
            conn.send(str(sendLoc))
            # Receive ACK from client
            conn.settimeout(0.0)
            error_tolerance = 0
            for x in xrange(5):
                try:
                    time.sleep(0.3)
                    signal = conn.recv(1024)
                except socket.error, e:
                    err = e.args[0]
                    if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                        print 'try again'
                        error_tolerance = error_tolerance + 1
                    else:
                        print e
                        sys.exit(1)
                else: 
                    if signal == 'y':
                        break
            # Drop connection when reaches destination
            # or does not receive connection from client
            if error_tolerance == 5 or currentLoc == destination:
                print "Connection is dropped."
                conn.close()
                break

