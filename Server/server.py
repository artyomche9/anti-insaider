import socket
import select
import cv2
import numpy
import os
import face_recognition as face
import sending as send
import smtplib
import datetime
import sqlite3
import warnings
warnings.simplefilter("ignore", DeprecationWarning)

#print(datetime.datetime.now())
f = open('config.txt', 'r')
config = f.read()
config = config.split('\n')
TCP_IP = config[0]
TCP_PORT = int(config[1])
connected_clients_sockets = []

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def get_data():
    try:
        length = recvall(conn,16)
        sign = recvall(conn,int(length))
        #sign = sign.decode()
        length = recvall(conn,16)
        stringData = recvall(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        #server_socket.close()
        return data,sign
    except:
        return None

def save(data,host):
    decimg = cv2.imdecode(data,1)
    name = host +'.png'
    cv2.imwrite(name, decimg)
    #cv2.imshow('SERVER',decimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return name 

def send_data(data):
    sock = socket.socket()
    sock.connect((TCP_IP, TCP_PORT+1))
    sock.send( str(len(data)).ljust(16).encode())
    sock.send(data.encode())
    sock.close()



def add_to_datbase(log):
    conn = sqlite3.connect("database.db") 
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE logs
                        (date text, result text, host text, login text, face text)
                    """)
    except:
        pass
    
    cursor.execute("INSERT INTO logs VALUES (?,?,?,?,?)", log)
    conn.commit()
    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((TCP_IP, TCP_PORT))
server_socket.listen(True)

connected_clients_sockets.append(server_socket)

while True:
    read_sockets, write_sockets, error_sockets = select.select(connected_clients_sockets, [], [])
    for sock in read_sockets:
        if sock == server_socket:
            conn, addr = server_socket.accept()
            connected_clients_sockets.append(conn)
        else:
            try:
                img,signature = get_data()
                signature = signature.decode()
                signature = signature.split('#')
                path = save(img,signature[1])
                user = face.recognize(path)
                if user == signature[0]:
                    send_data('1')
                    os.remove(path)
                    result = 'True'
                else:
                    send_data('0')
                    result = 'False'
                    number = 'your phone'
                    mail = 'your e-mail'
                    mess = 'Зарегистрирован нелигитимный вход в аккаунт '+ signature[0] + ' на машне' + signature[1]
                    #send.SMS(number,mess)
                    #send.email(mail,mess)
                time = str(datetime.datetime.now())
                time = time[:time.index('.')]
                log = [time,result,signature[1],signature[0],user]
                add_to_datbase(log)
                


                
            except:
                sock.close()
                connected_clients_sockets.remove(sock)
                continue


server_socket.close()