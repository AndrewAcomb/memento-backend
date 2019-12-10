from socket import *
import os

glassClientSocket = socket(AF_INET, SOCK_STREAM)
glassPort = 8088
#glassClientSocket.connect(('localhost', glassPort))
glassClientSocket.connect(('3.134.84.232', glassPort))

try:
    size = os.stat("sample.jpg").st_size
    glassClientSocket.sendall(("SIZE " + str(size)).encode())
    response = glassClientSocket.recv(1024).decode()

    print("client response = " + response)

    if response == "GOT SIZE":
        
        imageFile = open("sample.jpg", 'rb')
        sent_size = 0
        while sent_size != size:
            imageBytes = imageFile.read(1024)
            glassClientSocket.sendall(imageBytes)
            sent_size += len(imageBytes)
        imageFile.close()

        response = glassClientSocket.recv(1024).decode()

        print("client response = " + response)

finally:
    glassClientSocket.close()

