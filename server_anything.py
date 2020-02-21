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
                
            readable, writable, exceptional = select(inputs, [], inputs)

            for s in exceptional:
                inputs.remove(s)
                s.close()
            
            for s in readable:
                if s is self.glassServerSocket:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                    print("Glass client " + str(conn.getpeername()) + " connected!")
                else:
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        request = data.decode()
                        if request.startswith('POST'):
                            print("Glass client " + str(s.getpeername()) + " HTTP POST spam request. Connection shut down.")
                            inputs.remove(s)
                            s.close()
                        elif request != "":
                            print("Glass client " + str(s.getpeername()) + " request: " + request)
                            s.sendall("GOT REQUEST".encode())
                        else:
                            print("Glass client " + str(s.getpeername()) + " shut down connection.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(e)
                        inputs.remove(s)
                        s.close()

        self.glassServerSocket.close()


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
                
            readable, writable, exceptional = select(inputs, [], inputs)

            for s in exceptional:
                inputs.remove(s)
                s.close()
            
            for s in readable:
                if s is self.phoneServerSocket:
                    conn, addr = s.accept()
                    conn.setblocking(0)
                    inputs.append(conn)
                    print("Phone client " + str(conn.getpeername()) + " connected!")
                else:
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        request = data.decode()
                        if request.startswith('POST'):
                            print("Phone client " + str(s.getpeername()) + " HTTP POST spam request. Connection shut down.")
                            inputs.remove(s)
                            s.close()
                        elif request != "":
                            print("Phone client " + str(s.getpeername()) + " request: " + request)
                            s.sendall("GOT REQUEST".encode())
                        else:
                            print("Phone client " + str(s.getpeername()) + " shut down connection.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(e)
                        inputs.remove(s)
                        s.close()

        self.phoneServerSocket.close()


server = Server()
server.runServer()