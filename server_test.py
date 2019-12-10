# import kairos library
# from database import Database
from socket import * 
from select import *
import threading
import _thread


class Server(object):

    def __init__(self):
        print("__init__:")
        self.glassServerSocket = socket(AF_INET, SOCK_STREAM) # for handling request from google glass
        #self.phoneServerSocket = socket(AF_INET, SOCK_STREAM) # for handling request from cell phone
        self.glassPort = 8088
        #self.phonePort = 8089
    

    def runServer(self):
        print("runServer:")
        glassServerThread = threading.Thread(target=Server.startGlassServer, args=(self,))
        #phoneServerThread = threading.Thread(target=Server.startPhoneServer, args=(self,))
        glassServerThread.start()
        #phoneServerThread.start()
        print("server is running!")


    def startGlassServer(self):
        print("startGlassServer:")
        
        self.glassServerSocket.setblocking(0)
        self.glassServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        #self.glassServerSocket.bind(("localhost", self.glassPort))
        self.glassServerSocket.bind((gethostname(), self.glassPort))
        print("GlassServerSocket binded to port: ", self.glassPort)
        self.glassServerSocket.listen(5)
        print("GlassServerSocket is listening")

        inputs = [self.glassServerSocket]

        while inputs:

            if len(inputs) == 1:

                status = input("listen to next client? (Y/N)")

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
                        if request.startswith('SIZE'):
                            strings = request.split()
                            size = int(strings[1])
                            print("Got size: " + str(size))
                            conn.sendall("GOT SIZE".encode())

                            imageFile = open("received.jpg", 'wb')
                            received_size = 0
                            while received_size != size:
                                data = s.recv(1024)
                                imageFile.write(data)
                                received_size += len(data)
                            print("Got image")
                            imageFile.close()
                            conn.sendall("GOT IMAGE".encode())
                        s.close()
                    except Exception as e:
                        print(e)
                        s.close()

        self.glassServerSocket.close()

    def startPhoneServer(self):
        print("startPhoneServer:")
        

server = Server()
server.runServer()
