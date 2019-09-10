import socket
import cv2
import numpy
import os
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from datetime import datetime, date, time


class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        client()

#if __name__ == '__main__':
    #win32serviceutil.HandleCommandLine(AppServerSvc)


login = os.environ.get("USERNAME")
computer = socket.gethostname()
signature = login + '#' + computer

f = open('config.txt', 'r')
config = f.read()
config = config.split('\n')
TCP_IP = config[0]
TCP_PORT = int(config[1])

sock = socket.socket()
try:
    sock.connect((TCP_IP, TCP_PORT))
except:
    import winlock

def take_photo():

    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()

    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    return stringData

def send_data(data,signature):
    sock.send( str(len(signature)).ljust(16).encode())
    sock.send(signature.encode())
    sock.send( str(len(data)).ljust(16).encode())
    sock.send(data)
    #sock.close()

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def get_data():
    recieve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    recieve_socket.bind((TCP_IP, TCP_PORT+1))
    recieve_socket.listen(True)
    conn, addr = recieve_socket.accept()
    #sign = sign.decode()
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    #data = numpy.fromstring(stringData, dtype='uint8')
    #server_socket.close()
    return stringData.decode()


def client():
    #msg = computer + '#' + login
    #send_data(msg)
    photo = take_photo()
    send_data(photo,signature)
    answer = get_data()
    sock.close()
    #decimg=cv2.imdecode(data,1)
    #cv2.imshow('CLIENT',decimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows() 

    if answer == '1':
        print(computer)
    else:
        import winlock

if False:
    win32serviceutil.HandleCommandLine(AppServerSvc)
client()

