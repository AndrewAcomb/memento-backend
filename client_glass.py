from socket import *

glassClientSocket = socket(AF_INET, SOCK_STREAM)
glassPort = 8088
#glassClientSocket.connect(('localhost', glassPort))
glassClientSocket.connect(('3.19.14.13', glassPort))

try:
    imageFile = open("sample.jpg", 'rb')
    imageBytes = imageFile.read()
    size = len(imageBytes)
    imageFile.close()

    glassClientSocket.sendall(("SIZE " + str(size)).encode())

    glassClientSocket.sendall(imageBytes)

    response = glassClientSocket.recv(1024).decode()

    print("server response = " + response)
        

finally:
    glassClientSocket.close()

