from socket import * 
from select import *
import threading
import _thread
import os
import glob
import json

class Server(object):

    def __init__(self):
        print("Initializing:\n")
        self.glassServerSocket = socket(AF_INET, SOCK_STREAM)
        self.phoneServerSocket = socket(AF_INET, SOCK_STREAM)
        self.glassPort = 8088
        self.phonePort = 8089
    

    def runServer(self):
        glassServerThread = threading.Thread(target=Server.startGlassSocket, args=(self,))
        glassServerThread.start()
        phoneServerThread = threading.Thread(target=Server.startPhoneSocket, args=(self,))
        phoneServerThread.start()


    def startPhoneSocket(self):
        print("Start Phone Socket:")

        self.phoneServerSocket.setblocking(0)
        self.phoneServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        #self.phoneServerSocket.bind(("127.0.0.1", self.phonePort))
        self.phoneServerSocket.bind((gethostbyname(gethostname()), self.phonePort))
        print("\nPhoneServerSocket binded to IP: ", gethostbyname(gethostname()))
        print("PhoneServerSocket binded to port: ", self.phonePort)
        self.phoneServerSocket.listen(5)
        print("PhoneServerSocket is listening\n")

        inputs = [self.phoneServerSocket]

        while inputs:

            if len(inputs) == 1:

                status = input("No phone connected! Listen to another phone? (Y/N)")

                if status == "n" or status == "N":
                    break
                
                if status != "y" and status != "Y":
                    continue
                
            readable, writable, exceptional = select(inputs, [], inputs)

            for s in exceptional:
                inputs.remove(s)
                s.close()
            
            for s in readable:
                if s is self.phoneServerSocket:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                else:
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        #print("bytes received:")
                        #print(data)
                        request = data.decode()
                        if request != "":
                            print("client " + str(s.getpeername()) + " request: " + request)
                            s.sendall("GOT REQUEST".encode())
                        else:
                            print("client " + str(s.getpeername()) + " shut down connection.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(e)
                        s.close()

        self.phoneServerSocket.close()



    def startGlassSocket(self):
        print("Start Glass Socket:")
        
        self.glassServerSocket.setblocking(0)
        self.glassServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        #self.glassServerSocket.bind(("127.0.0.1", self.glassPort))
        self.glassServerSocket.bind((gethostbyname(gethostname()), self.glassPort))
        print("\nGlassServerSocket binded to IP: ", gethostbyname(gethostname()))
        print("GlassServerSocket binded to port: ", self.glassPort)
        self.glassServerSocket.listen(5)
        print("GlassServerSocket is listening\n")

        inputs = [self.glassServerSocket]

        while inputs:

            if len(inputs) == 1:

                status = input("No glass connected! Listen to another glass? (Y/N)")

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
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        #print("bytes received:")
                        #print(data)
                        request = data.decode()
                        if request != "":
                            print("client " + str(s.getpeername()) + " request: " + request)
                            s.sendall("GOT REQUEST".encode())
                        else:
                            print("client " + str(s.getpeername()) + " shut down connection.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(e)
                        s.close()

        self.glassServerSocket.close()


server = Server()
server.runServer()