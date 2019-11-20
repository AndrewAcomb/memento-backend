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
        
        self.glassServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        self.glassServerSocket.bind(('localhost', self.glassPort))
        print("GlassServerSocket binded to port: ", self.glassPort)
        self.glassServerSocket.listen(1)
        print("GlassServerSocket is listening")

        while True:
            
            conn, addr = self.glassServerSocket.accept()
                
            try:
                print("handleGlassConnection:")
                data = conn.recv(4096)
                request = data.decode()
                if request.startswith('SIZE'):
                    strings = request.split()
                    size = int(strings[1])
                    print("Got size: " + str(size))
                    conn.send("GOT SIZE".encode())
                    data = conn.recv(40960000)
                    if data:
                        print("Got image")
                        imageFile = open("receive/received.png", 'wb')
                        imageFile.write(data)
                        imageFile.close()
                        conn.send("GOT IMAGE".encode())
                        conn.shutdown(SHUT_WR) # instead of shutting down connection immediately, get the names with the help of Kairos and send them back
                elif request.startswith('CLOSE'):
                    print("Got close")
                    conn.shutdown(SHUT_WR)
            except:
                conn.shutdown(SHUT_WR)
                continue

        self.glassServerSocket.close()


    def startPhoneServer(self):
        print("startPhoneServer:")
        

server = Server()
server.runServer()