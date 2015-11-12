from readTag import TagInfo
import socket
import time
import serial
import sys
import errno

# Define some parameters
BITS = 6
HOST = '192.168.23.2'

def readNextCommand(currentLoc, currentAngle, currentDis, destination):
    ########################################################
    # Given the current location and the target, 
    # return the next command and the next location
    # When the command the turning, target should be same,
    # otherwise, target is the next position.
    # 
    ########################################################
    command = input('What is the command: [F, L, R, S]\n')
    offset = input('What is the offset: \n')
    target = input('What is the next target: \n')
    return command+offset, target

def decodeLoc(value, mask):
    ########################################################
    # Decode the location from the AprilTag value
    ########################################################
    value = (~value + (value << 21)) & mask
    value = value ^ value >> 24
    value = ((value + (value << 3)) + (value << 8)) & mask
    value = value ^ value >> 14
    value = ((value + (value << 2)) + (value << 4)) & mask
    value = value ^ value >> 28
    value = (value + (value << 31)) & mask
    return value

# Upon powering up, run main.py
print "Program starts."

# 1. readMap("Map.txt")

# 2. initialize socket, run server
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print "Server is on."

# Initialize uart
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
print "Uart established."

# Initialize camera
Tag = TagInfo()

while 1:
    # Listen for requests
    s.listen(1)
    # Connect to a client
    conn, addr = s.accept()    
    print('Connected to', addr)
    # Receive the destination location from the client.
    destination = int(conn.recv(1024))
    print "Receive destination: "+str(destination)
    # Get the start location and orientation
    error_tolerance = 0
    while 1:
        Tag.Capture()
        if Tag.TagDetected:
            currentLoc = decodeLoc(Tag.Value, (1<<BITS)-1)
            currentAngle = Tag.Orientation
            currentDis = Tag.Distance
            print "Location is: "+str(currentLoc)
            print "Distance is: "+str(Tag.Distance)
            print "Orientation is: "+str(currentAngle)
            break
        else:
            print "No tag detected."
            error_tolerance = error_tolerance + 1
            if error_tolerance == 5:
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
                time.sleep(0.2)
    # Start the main loop
    while 1:
        # Read the next target
        command, target = readNextCommand(currentLoc, currentAngle, currentDis, destination)
        print "Next command is: "+command
        # Send the command to MCU
        ser.write(command)
        ACK = ser.read() # TODO: Check if command is lost or incorrect
        # Receive the signal from MCU when reaching target
        signal = ser.read()
        # If MCU says if finishes
        # TODO: check if too long time without a signal
        if signal == 'f':
            # Sample a Tag to see if really finishes
            error_tolerance = 0
            while 1:
                Tag.Capture()
                if Tag.TagDetected:
                    currentLoc = decodeLoc(Tag.Value, (1<<BITS)-1)
                    currentAngle = Tag.Orientation
                    currentDis = Tag.Distance
                    print "Location is: "+str(currentLoc)
                    print "Distance is: "+str(Tag.Distance)
                    print "Orientation is: "+str(currentAngle)
                if Tag.TagDetected==0 or target!=currentLoc:
                    if Tag.TagDetected==0:
                        print "No tag detected."
                    else:
                        print "Location does not match: "+str(target)+". Resample image."
                    error_tolerance = error_tolerance + 1
                    if error_tolerance == 5:
                        getInput = raw_input("Which loc do you want to set? Press enter to continue.\n")
                        if getInput == "":
                            error_tolerance = 0
                            time.sleep(0.2)
                        else:
                            # print "I am lost:(.. I am now at "+str(currentLoc)
                            # sys.exit(1)
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
                        time.sleep(0.2)
            # Delete after
            if target!=currentLoc:
                print "I am lost:(.. I am now at "+str(currentLoc)
                sys.exit(1)
            # Reaches target. Send position update to client
            conn.send(str(currentLoc))
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

