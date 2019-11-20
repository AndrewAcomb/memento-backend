from socket import *

glassClientSocket = socket(AF_INET, SOCK_STREAM)
glassPort = 8088
glassClientSocket.connect(('127.0.0.1', glassPort))

try:
    imageFile = open("sample.jpg", 'rb')
    imageBytes = imageFile.read()
    size = len(imageBytes)
    imageFile.close()

    glassClientSocket.sendall(("SIZE " + str(size)).encode())
    response = glassClientSocket.recv(4096).decode()

    print("response = " + response)

    if response == "GOT SIZE":

        glassClientSocket.sendall(imageBytes)
        response = glassClientSocket.recv(4096).decode()

        print("response = " + response)

        if response == "GOT IMAGE":
            glassClientSocket.sendall("CLOSE".encode())

            print("Image Sent!")

finally:
    glassClientSocket.close()

