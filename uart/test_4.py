#!/usr/bin/python
import serial
import time
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
print "finish"
while True:
   ser.write(b"he")
   print "1"
   #time.sleep(0.1)
   data = ser.read(2)
   print data
   time.sleep(1)


