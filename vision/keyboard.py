from vision import *
import socket
import time
import serial
import errno
import exmod
import sys
import RPi.GPIO as GPIO

PIN  = 18
# Define some parameters
HOST = '35.2.34.87'

# Upon powering up, run main.py
print "Program starts."

# initialize socket, run server
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print "Server is on."

# Initialize uart
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
print "Uart established."

# Initialize camera
camera = TagCamera()
print "camera is on."
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)
GPIO.output(PIN, GPIO.LOW)
print "GPIO" + str(PIN) + "set up to output." 

while 1:
    # Listen for requests
    s.listen(1)
    # Connect to a client
    conn, addr = s.accept()    
    print('Connected to', addr)
    # Receive the destination location from the client.
    destination = decodeLoc(int(conn.recv(1024)))
    print "Receive destination: "+str(destination)
    # Start the main loop
    while 1:
        # Detect current location
        detected, currentLoc, currentAngle, currentDis = camera.getTagInfo()

        #G, H, I, J, K adjust to move forward;
        #B, C, D, E, F adjust to move backward;
        #M adjust to turn left
        #T adjsut to turn right
        #A move forward;
        #L turn left;
        #R turn right; 


        command_keyboard = raw_input("Enter your next command from keyboard: ")

        print "GPIO is low"
        GPIO.output(PIN, GPIO.LOW)
        print "GPIO is high"
        GPIO.output(PIN, GPIO.HIGH)
       
            
        ser.write(command_keyboard)
        print "command" + command_keyboard +"  was just written."

        signal = ser.read()
        print "ACK signal received: " + signal
        if signal  == command_keyboard:
            GPIO.output(PIN, GPIO.LOW)
            print "GPIO is low"
            


        if detected:
            sendLoc = currentLoc[0]*NUMCOL + currentLoc[1]
            conn.send(str(sendLoc))
            print "send loc to client"
            # Receive ACK from client
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
            # Drop connection when reaches destination
            # or does not receive connection from client
            # if error_tolerance == 5:
            #     print "Connection is dropped."
            #     conn.close()
            #     break
            if currentLoc == destination and abs(currentDis[0]) < 5:
                print "Finished. Connection is dropped."
                conn.close()
                break

