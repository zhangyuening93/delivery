from readTag import TagInfo
import socket
import time
import serial


# Upon powering up, run main.py
print "Program starts."

# 1. readMap("Map.txt")

# 2. initialize socket, run server
HOST = ''
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
    destination = conn.recv(1024)
    # Get the start location.
    Tag.Capture()
    if Tag.TagDetected:
        print "Distance: "+ str(Tag.Distance)
        print "Orientation: "+ str(Tag.Orientation)
        print "Value: "+ str(Tag.Value)
        currentLoc = Tag.Value
    else:
        print "No tag detected."
        currentLoc = 0
    # Start the main loop
    while 1:
        # Read the next target
        command, target = readNextPosition(currentLoc, destination)
        # Send the command to MCU
        ser.write(command)
        ACK = ser.read() # TODO: Check if command is lost or incorrect
        # Receive the signal from MCU when reaching target
        signal = ser.read()
        if signal == 'f':
            Tag.Capture()
            if Tag.TagDetected():
                print "Distance: "+ str(Tag.Distance)
                print "Orientation: "+ str(Tag.Orientation)
                print "Value: "+ str(Tag.Value)
                currentLoc = Tag.Value
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
            conn.send(currentLoc)
        if target == position:
            conn.close()
            break

#       if wait for too long
#           raise error to client
#       if finish
#           if not des
#               update position to client
#           if des
#               update status to client and disconnet, break


def readNextPosition(currentLoc, destination):
    ########################################################
    # Given the current location and the target, 
    # return the next command and the next location
    ########################################################
    command = input('What is the command: [F, L, R, S]\n')
    offset = input('What is the offset: \n')
    target = input('What is the next target: \n')
    return str(command)+str(offset), str(target)




def decodeLoc(value):
    ########################################################
    # Decode the location from the AprilTag value
    ########################################################
    return value