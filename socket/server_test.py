# Echo server program
import socket
import errno
import time
import sys

HOST = socket.gethostname()                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while 1:
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(1024)
    print data
    while 1:
        # if not data: break
        data = input("send what?\n")
        conn.send(data)
        conn.settimeout(0.0)
        error_tolerance = 0
        for x in xrange(5):
            try:
                signal = conn.recv(1024)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                # if err == 107:
                    # time.sleep(1)
                    print 'try again'
                    error_tolerance = error_tolerance + 1
                    time.sleep(1)
                else:
                    # a "real" error occurred
                    print e
                    sys.exit(1)
            else: 
                if signal == 'y':
                    break
                # elif signal == 'f':
                #     error_tolerance = 5
                #     break
        if error_tolerance == 5 or data == '10':
            print "Connection is dropped."
            conn.close()
            break