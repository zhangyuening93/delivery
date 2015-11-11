from readTag import TagInfo
import socket
import time
import serial
import sys
import errno

def readNextPosition(currentLoc, destination):
    ########################################################
    # Given the current location and the target, 
    # return the next command and the next location
    ########################################################
    command = input('What is the command: [F, L, R, S]\n')
    offset = input('What is the offset: \n')
    # target = input('What is the next target: \n')
    target = 0
    return command+offset, str(target)

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
#HOST = ''
HOST = '192.168.23.2'
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
    # destination = conn.recv(1024)
    destination = 0
    # Get the start location.
    Tag.Capture()
    if Tag.TagDetected:
        print "Distance: "+ str(Tag.Distance)
        print "Orientation: "+ str(Tag.Orientation)
        print "Value: "+ str(Tag.Value)
        currentLoc = decodeLoc(Tag.Value, (1<<8)-1)
    else:
        print "No tag detected."
        currentLoc = 0
    # Start the main loop
    while 1:
        # Read the next target
        command, target = readNextPosition(currentLoc, destination)
        print command
        # Send the command to MCU
        ser.write(command)
        ACK = ser.read() # TODO: Check if command is lost or incorrect
        # Receive the signal from MCU when reaching target
        signal = ser.read()
        # If MCU says if finishes
        # TODO: check if too long time without a signal
        if signal == 'f':
            # Sample a Tag to see if really finishes
            Tag.Capture()
            if Tag.TagDetected:
                print "Distance: "+ str(Tag.Distance)
                print "Orientation: "+ str(Tag.Orientation)
                print "Value: "+ str(Tag.Value)
                currentLoc = decodeLoc(Tag.Value, (1<<8)-1)
            else:
                print "No tag detected."
                currentLoc = 0
            # TODO: Need to make corrections
            # error_tolerance = 0
            # for x in xrange(5):
            #     Tag.capture()
            #     if Tag.TagDetected:
            #         print "Distance: "+ str(Tag.Distance)
            #         print "Orientation: "+ str(Tag.Orientation)
            #         print "Value: "+ str(Tag.Value)
            #         break
            #     else:
            #         error_tolerance = error_tolerance + 1
            #     time.sleep(0.5)
            # if error_tolerance == 5:
            #     print "Tag is not recognized. Please check where I am :("
            if target!=currentLoc:
                # Try again 5 times
                print "I am lost. I am now at "+str(currentLoc)
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

#       if wait for too long
#           raise error to client
#       if finish
#           if not des
#               update position to client
#           if des
#               update status to client and disconnet, break



