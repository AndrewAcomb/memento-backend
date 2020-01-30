from socket import *

glassClientSocket = socket(AF_INET, SOCK_STREAM)
glassPort = 8088
#glassClientSocket.connect((gethostbyname(gethostname()), glassPort))
glassClientSocket.connect(('3.134.84.232', glassPort))
#glassClientSocket.connect(('127.0.0.1', glassPort))

try:

    glassClientSocket.sendall("Hello".encode())
    response = glassClientSocket.recv(1024).decode()

    print("server response = " + response)
        

finally:
    glassClientSocket.close()

