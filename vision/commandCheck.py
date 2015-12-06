#from vision import *
import socket
import time
import serial
import errno
import exmod
import sys
import RPi.GPIO as GPIO

MyCommand = "ABSLR"
idx = 0

def NextCommand(idx):
    if idx < 5:
        result = MyCommand[idx]
        idx = idx+1
    return result

PIN  = 24
# Define some parameters
HOST = socket.gethostname()


# Upon powering up, run main.py
print "Program starts."

# initialize socket, run server
#PORT = 50007
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))
#print "Server is on."

# Initialize uart
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
print "Uart established."

# Initialize camera
#camera = TagCamera()
#print "camera is on."
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)
print "GPIO" + str(PIN) + " set up to output." 

while 1:
    # Listen for requests
    # s.listen(1)
    # Connect to a client
    # conn, addr = s.accept()    
    # print('Connected to', addr)
    # Receive the destination location from the client.
    # destination = decodeLoc(int(conn.recv(1024)))
    # print "Receive destination: "+str(destination)
    # Start the main loop
    while 1:
        # Detect current location
        # detected, currentLoc, currentAngle, currentDis = camera.getTagInfo()
        # if not detected:
            # print "I am lost at initial position."
            # conn.send('F')
            # print "Connection is dropped."
            # conn.close()
            # continue
        # if detected:
        # Get the path
            # path = exmod.find_route(currentLoc[0], currentLoc[1], destination[0],destination[1])
            # print path
            # Read the next target
        command= NextCommand(idx)
        print "Next command is: "+command
        # Send the command to MCU
        # Set GPIO
        
        GPIO.output(PIN, GPIO.LOW)
        GPIO.output(PIN, GPIO.HIGH)
        while 1:
            ser.write(command)
            signal = ser.read()
            if signal == command:
               GPIO.output(PIN, GPIO.LOW)
               break

        # if command=='L' or command == 'R':
        if idx == 5:
            sys.exit(0)
        time.sleep(3)

        #signal = 'f'
        # If MCU says if finishes
        # TODO: check if too long time without a signal
        # if signal == 'f':
            # Sample a Tag to see if really finishes
            # detected, currentLoc, currentAngle, currentDis = camera.getTagInfo()
            # Delete after
            # if not detected:
            #     print "I am lost:(.."
            #     conn.send('F')
            #     print "Connection is dropped."
            #     conn.close()
            #     break
            # if target!=currentLoc:
            #     print "I am lost:(.. I am now at "+str(currentLoc)
            #     conn.send('F')
            #     print "Connection is dropped."
            #     conn.close()
            #     break
            # Reaches target. Send position update to client
            # sendLoc = currentLoc[0]*NUMCOL + currentLoc[1]
            # conn.send(str(sendLoc))
            # # Receive ACK from client
            # conn.settimeout(0.0)
            # error_tolerance = 0
            # for x in xrange(5):
            #     try:
            #         time.sleep(0.3)
            #         signal = conn.recv(1024)
            #     except socket.error, e:
            #         err = e.args[0]
            #         if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            #             print 'try again'
            #             error_tolerance = error_tolerance + 1
            #         else:
            #             print e
            #             sys.exit(1)
            #     else: 
            #         if signal == 'y':
            #             break
            # # Drop connection when reaches destination
            # # or does not receive connection from client
            # if error_tolerance == 5:
            #     print "Connection is dropped."
            #     conn.close()
            #     break
            # if currentLoc == destination and abs(currentDis[0]) < 5:
            #     print "Connection is dropped."
            #     conn.close()
            #     break

