#!/usr/bin/python
import serial
import RPi.GPIO as gpio
import time
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 9600)
#gpio.cleanup()
#gpio.setmode(gpio.BOARD)
#gpio.setup(24,gpio.OUT)
mode = 0
while True:
   ser.write('h')
   print 'h is written.'
   data = ser.read()
   print data
   time.sleep(0.5)
   data = ser.read()
   print data
   #if data=='r':
      #if mode == 0:
         #gpio.output(24,True)
         #mode = 1
      #else:
         #gpio.output(24,False)
         #mode = 0
      
