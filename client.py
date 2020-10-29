import socket
import os
import subprocess

s = socket.socket() 
host = "192.168.1.104"
port = 9998

s.connect((host,port))
path = str(s.recv(1024),"utf-8")
print(path)
while True:
    cmd = input()
    if(cmd=="q"):
        s.close()
        break

    if(len(cmd) > 0):
        s.send(str.encode(cmd))
        client_response = str(s.recv(1024),"utf-8")
        print(client_response, end="")


