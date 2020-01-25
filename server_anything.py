from socket import * 
from select import *
import threading
import _thread
import cv2
import os
import glob
import json

class Server(object):

    def __init__(self):
        print("Initializing:\n")
        self.glassServerSocket = socket(AF_INET, SOCK_STREAM)
        self.glassPort = 8088
    

    def runServer(self):
        glassServerThread = threading.Thread(target=Server.startGlassSocket, args=(self,))
        glassServerThread.start()


    def startGlassSocket(self):
        print("Start Glass Socket:")
        
        self.glassServerSocket.setblocking(0)
        self.glassServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        self.glassServerSocket.bind((gethostbyname(gethostname()), self.glassPort))
        print("GlassServerSocket binded to IP: ", gethostbyname(gethostname()))
        print("GlassServerSocket binded to port: ", self.glassPort)
        self.glassServerSocket.listen(5)
        print("GlassServerSocket is listening\n")

        inputs = [self.glassServerSocket]

        while inputs:

            if len(inputs) == 1:

                status = input("receive next frame? (Y/N)")

                if status == "n" or status == "N":
                    break
                
                if status != "y" and status != "Y":
                    continue
                
            readable, writable, exceptional = select(inputs, [], inputs)

            for s in exceptional:
                inputs.remove(s)
                s.close()
            
            for s in readable:
                if s is self.glassServerSocket:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                else:
                    inputs.remove(s)
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        request = data.decode()
                        if request != "":
                            print("client request: " + request)
                            conn.sendall("GOT REQUEST".encode())
                        s.close()
                    except Exception as e:
                        print(e)
                        s.close()

        self.glassServerSocket.close()


server = Server()
server.runServer()