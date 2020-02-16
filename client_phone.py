from socket import *

phoneClientSocket = socket(AF_INET, SOCK_STREAM)
phonePort = 8089
#phoneClientSocket.connect(('localhost', phonePort))
phoneClientSocket.connect(('3.134.84.232', phonePort))

try:
    phoneClientSocket.sendall(("NEW 1".encode())
    response = phoneClientSocket.recv(1024).decode()

    if response.startswith('SIZE'):
        strings = response.split()
        size = int(strings[1])
        imageFile = open("unknown_from_server.jpg")
        received_size = 0
        while received_size != size:
            data = phoneClientSocket.recv(1024)
            imageFile.write(data)
            received_size += len(data)
        imageFile.close()
        print("got unknown face from server, named unknown_from_server.jpg")
    else: 
        print("server response = " + response)

finally:
    phoneClientSocket.close()

