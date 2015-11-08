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

# 3. while(1)
while 1:
#   listen(1)
    s.listen(1)
    conn, addr = s.accept()    
    print('Connected to', addr)
    target = conn.recv(1024)
#   while(1)
    while 1:
#       readNextPosition()
        command, position = readNextPosition(target)
#       serial.send()
        ser.write(command)
#       while not serial.receive()
        data = ser.read()
#           serial.send() 5 times
#       serial.read()
        data = ser.read()
        if data == 'f':
            error_tolerance = 0
            for x in xrange(5):
                Tag.capture()
                if Tag.TagDetected:
                    print "Distance: "+ str(Tag.Distance)
                    print "Orientation: "+ str(Tag.Orientation)
                    print "Value: "+ str(Tag.Value)
                    break
                else:
                    error_tolerance = error_tolerance + 1
                time.sleep(0.5)
            if error_tolerance == 5:
                print "Tag is not recognized. Please check where I am :("

            conn.send(position)
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

