#!/usr/bin/env python
from Tkinter import *
# import threading
import socket
# import numpy as np
import time
import errno
import math

NUMCOL = 6
NUMROW = 7
INIT_X = 0
INIT_Y = 0

class AppGUI(Frame):
    """This is the GUI application for computer terminal."""

    def __init__(self, master, pos_x=0, pos_y=0):
        # Initialize GUI

        Frame.__init__(self, master)

        # Initial configuration
        self.pos_x = pos_x
        self.pos_y = pos_y

        # Variables
        self._request_flag = 0
        self._destination = ""

        self.grid()
        self._create_widgets()

    def getRequest(self):
        return self._request_flag

    def resetRequest(self):
        self._request_flag = 0

    def getDestination(self):
        return self._destination
        
    def _create_widgets(self):
        self.canvas = Canvas(self, height=500, width=500, bg="white")
        self._configure_canvas()
        self.canvas.grid(row=1, column=1, columnspan=3)

        mycolor = '#40E0D0'

        self.button1 = Button(self, text="request", command=self.cb_request, bg=mycolor)
        self.button1.grid(row=2, column=1)

        self.entry = Entry(self)
        self.entry.grid(row=2, column=2)

        self.info = Text(self, height=33, width=50, wrap=WORD)
        self.info.grid(row=1, column=4)
       

    def _configure_canvas(self):
        self.car_shape = self.canvas.create_rectangle(int(500/NUMCOL*self.pos_y-10), int(500/NUMROW*self.pos_x-10), int(500/NUMCOL*self.pos_y+10), int(500/NUMROW*self.pos_x+10), fill="blue")
        self.car_text = self.canvas.create_text(int(500/NUMCOL*self.pos_y), int(500/NUMROW*self.pos_x), text="R")


    def updatePosition(self):
        self.canvas.delete(self.car_shape)
        self.canvas.delete(self.car_text)
        self.car_shape = self.canvas.create_rectangle(int(500/NUMCOL*self.pos_y-10), int(500/NUMROW*self.pos_x-10), int(500/NUMCOL*self.pos_y+10), int(500/NUMROW*self.pos_x+10), fill="blue")
        self.car_text = self.canvas.create_text(int(500/NUMCOL*self.pos_y), int(500/NUMROW*self.pos_x), text="R")

    def cb_request(self):
        if self._request_flag == 1:
            self.info.insert(0.0,"Request has not finished yet.\n")
        else:
            self.info.insert(0.0,"Send new request.\n")
            self._request_flag = 1
            self._destination = self.entry.get()
            self.entry.delete(0, END)


    def insertMsg(self, msg):
        self.info.insert(0.0,msg)


            
class AppTask(object):
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.root = Tk()
        self.root.title("Service")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.app = AppGUI(self.root, INIT_X, INIT_Y)

        # Flags
        # self._connected = 0

        self.root.after(1000, self.task)
        self.root.mainloop()

    def callback(self):
        self.root.quit()

    def task(self):
        print "In task."
        if self.app.getRequest():
            print "Send request!"
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((self.HOST, self.PORT))
            # self.s.send(b'Client: destination')
            self.s.send(self.app.getDestination())
            # self.Target = '10'
            self.root.after(500, self.getUpdate)
        else:
            self.root.after(1000, self.task)  # reschedule event in 2 seconds


    def getUpdate(self):
        print "In update."
        self.s.settimeout(0.0)
        try:
            data = self.s.recv(1024)
        except socket.error, e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                print 'No data available'
                self.root.after(500, self.getUpdate)
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            if data == "":
                msg = "Request finished.\n"
                self.app.insertMsg(msg)
                print "Finish."
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.app.resetRequest()
                self.root.after(1000, self.task)
            elif data == 'F':
                msg = "I am lost. Please find me at ("+str(self.app.pos_x)+', '+str(self.app.pos_y)+").\n"
                self.app.insertMsg(msg)
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.app.resetRequest()
                self.root.after(1000, self.task)
            else:
                print "Update Position."
                data = int(data)
                self.app.pos_x = math.floor(data/NUMCOL)
                self.app.pos_y = data%NUMCOL
                self.app.updatePosition()
                msg = "Current position at ("+str(self.app.pos_x)+', '+str(self.app.pos_y)+").\n"
                self.app.insertMsg(msg)
                self.s.send(b'y')
                self.root.after(500, self.getUpdate)





if __name__=="__main__":
    # Initial socket
    HOST = '35.2.34.87'    # The remote host
    PORT = 50007              # The same port as used by the server

    # Initial App
    app = AppTask(HOST, PORT)

    
