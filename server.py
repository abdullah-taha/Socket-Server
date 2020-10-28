import socket
import sys
import threading 
from queue import Queue
num_of_threads = 2
job_num = [1,2]

host = ""
port = 9998


def create_socket():
    try:
        global s
        s = socket.socket()


    except socket.error as msg:
        print("Socket creation error"+ str(msg))


def bind_socket():
    global s
    try:
        print("Binding the port " + str(port))
        s.bind((host,port))
        print("Listesning...")
        s.listen(5)
    
    except socket.error as msg:
        print("Socket binding error"+ str(msg) +'\n' + "retrying..")
        bind_socket()


def socket_accept():
    conn,addres = s.accept()
    print("connection estableshed. IP: "+addres[0] + ", port: "+str(addres[1]))
    send_command(conn)
    conn.close()

def send_command(conn):
    while True:
        cmd = input()

        if(cmd=="q"):
            conn.close()
            s.close()
            sys.exit()

        if(len(str.encode(cmd)) > 0):
            conn.send(str.encode(cmd))
            client_response = str(conn.recv(1024),"utf-8")
            print(client_response, end="")

def main():
    create_socket()
    bind_socket()
    socket_accept()

main()