import socket
import sys
import threading 
import os
import subprocess
import threading

host = ""
port = 9998

class Server:
    def __init__(self):
        # initialize the Server class by creating the socket
        self.s = None
        self.binded = False
        try:
            self.s = socket.socket()
        except socket.error as msg:
            print("Socket creation error"+ str(msg))

    def bind_socket(self, host, port):
        # binds the defined socket to the specified host and port and start listening at the specific port
        # if binding failed, the error is printed to the screen and binding is tried again untill success
        try:
            print("Binding the port " + str(port))
            self.s.bind((host,port))
            self.s.listen(5)
            self.binded = True
            print("Listening...")
        
        except socket.error as msg: 
            print("Socket binding error"+ str(msg) +'\n' + "retrying..")
            self.bind_socket(host, port)

    def receive_command(self,conn):
        # recieve the incoming messages from the connection, creates a subprocess, execute the given command in the file system,
        # send the output through the socket
        # it also handles cd commands for different users by using a relative temporary directory for each command without changing the system working directory

        # print(threading.current_thread().name)
        os.chdir("D:\\Faraday")
        cwd = os.getcwd()
        conn.send(str.encode(cwd+ "> "))
        #  print(cwd)
        while True:
            data = conn.recv(1024)
            if not data:
                print("clinet disconnected")
                conn.close()
                break
            if(data[:2].decode("utf-8") == "cd"):
                cwd = os.path.abspath(cwd +"\\"+ data[3:].decode("utf-8"))
                #os.chdir(data[3:].decode("utf-8"))
                #print(cwd)
                conn.send(str.encode(cwd+ "> "))
            elif(len(data)>0):
                cmd = subprocess.Popen(data[:].decode("utf-8"),shell=True,  stdout = subprocess.PIPE, stdin = subprocess.PIPE, stderr=subprocess.PIPE,cwd=cwd)
                if(data[:2].decode("utf-8") == "cd"):
                    output_str=""
                else:
                    output_byte = cmd.stdout.read() + cmd.stderr.read()
                    output_str = str(output_byte,"utf-8")
                current_wd = cwd + "> "
                conn.send(str.encode(output_str + current_wd))
                print(output_str)

    def socket_accept(self,client, connection):
        # print the new connection and closed connection to the screen, closes the connection when aborted
        ip = connection[0]
        port = connection[1]
        print(f"New connection was made from IP: {ip}, and port: {port}!")
        self.receive_command(client)
        print(f"The client from ip: {ip}, and port: {port}, has diconnected!")
        client.close()


def main():
    # initiliaze a Server object, bind the socket to the given host and port, and call a seperate therad for each connected client
    x = Server()
    x.bind_socket(host,port)
    while True:
        try: 
            client, ip = x.s.accept()
            threading._start_new_thread(x.socket_accept,(client, ip))
        except KeyboardInterrupt:
            print(f"Shutting down the server!")
        except Exception as e:
            print(f"error : {e}")


main()