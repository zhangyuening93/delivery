#!/usr/bin/env python

import serial
import string

rot13 = string.maketrans( 
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz", 
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")

test=serial.Serial("/dev/ttyAMA0",9600)
test.open()

try:
    while True:
                line = test.readline(eol='\r')
                test.write(string.translate(line, rot13))
                
except KeyboardInterrupt:
    pass # do cleanup here

test.close()
