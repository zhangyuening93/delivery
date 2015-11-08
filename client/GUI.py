#!/usr/bin/env python
from Tkinter import *
# import threading
import socket
# import numpy as np
import time
import errno



class AppGUI(Frame):
    """This is the GUI application for computer terminal."""

    def __init__(self, master, pos_x=50, pos_y=50):
        # Initialize GUI

        Frame.__init__(self, master)

        # Initial configuration
        self._pos_x = pos_x
        self._pos_y = pos_y

        # Variables
        self._request_flag = 0

        self.grid()
        self._create_widgets()

    def getRequest(self):
        return self._request_flag

    def resetRequest(self):
        self._request_flag = 0
        
    def _create_widgets(self):
        self.canvas = Canvas(self, height=500, width=500, bg="white")
        self._configure_canvas()
        self.canvas.grid(row=1, column=1, columnspan=3)

        mycolor = '#40E0D0'

        self.button1 = Button(self, text="", command=self.cb_request, bg=mycolor)
        self.button1.grid(row=2, column=1)

        self.info = Text(self, height=33, width=50, wrap=WORD)
        self.info.grid(row=1, column=4)
       

    def _configure_canvas(self):
        self.shape = self.canvas.create_rectangle(self._pos_x-10, self._pos_y-10, self._pos_x+10, self._pos_y+10, fill="blue")
        self.text = self.canvas.create_text(self._pos_x, self._pos_y, text="R")


    def updatePosition(self, pos_x, pos_y):
        self.canvas.delete(self.car_shape)
        self.canvas.delete(self.car_text)
        self.car_shape = self.canvas.create_rectangle(pos_x-10, pos_y-10, pos_x+10, pos_y+10, fill="blue")
        self.car_text = self.canvas.create_text(pos_x, pos_y, text="R")

    def cb_request(self):
        if self._request_flag == 1:
            self.info.insert(0.0,"Request has not finished yet.\n")
        else:
            self.info.insert(0.0,"Send new request.\n")
            self._request_flag = 1
        # self.button1.configure(bg="red")
        # self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)
        
    # def display_message(self, message):
    #     self.info.insert(0.0, message)

    # def update_button(self, req_1, req_2, req_3):
    #     # print "will update button now."
    #     mycolor = '#40E0D0'
    #     if req_1:
    #         self.button1.configure(bg=mycolor)
    #         self.req_1_status = 0
    #     if req_2:
    #         self.button2.configure(bg=mycolor)
    #         self.req_2_status = 0
    #     if req_3:
    #         self.button3.configure(bg=mycolor)
    #         self.req_3_status = 0
    #     # print "button should be updated now."
    #     self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)



    # def callback_pub_1(self):
    #     self.req_2_status = 1
    #     self.button2.configure(bg="red")
    #     self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)

    # def callback_pub_2(self):
    #     self.req_3_status = 1
    #     self.button3.configure(bg="red")
    #     self.pub.publish(self.req_1_status, self.req_2_status, self.req_3_status)

            
class AppTask(object):
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.root = Tk()
        self.root.title("Service")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.app = AppGUI(self.root)

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
            self.s.send(b'I need the robot!')
            self.Target = '10'
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
                # time.sleep(1)
                print 'No data available'
                self.root.after(500, self.getUpdate)
            else:
                # a "real" error occurred
                print e
                sys.exit(1)
        else:
            if data == self.Target:
                print "Finish."
                self.s.send(b'f')
                self.s.shutdown(socket.SHUT_RDWR)
                self.s.close()
                self.app.resetRequest()
                self.root.after(1000, self.task)  # reschedule event in 2 seconds
            else:
                print "Update Position."
                self.s.send(b'y')
                self.root.after(500, self.getUpdate)





if __name__=="__main__":
    # Initial socket
    HOST = socket.gethostname()    # The remote host
    PORT = 50007              # The same port as used by the server

    # Initial App
    app = AppTask(HOST, PORT)

    