import kairos_face
# from database import Database
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
        print("__init__:")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        kairos_face.settings.app_id = "8af0a9da"
        kairos_face.settings.app_key = "e24042917823dd0e625ecb500f4f9e44"
        self.initKairos()
        self.analyzeFrame("image/glass_image/frame.jpg")
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
            
            status = input("listen to next client? (Y/N)")

            if status == "n" or status == "N":
                break
            
            if status != "y" and status != "Y":
                continue
            
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
                        imageFile = open("image/glass_image/frame.jpg", 'wb')
                        imageFile.write(data)
                        imageFile.close()
                        conn.send("GOT IMAGE".encode())
                        self.analyzeFrame("image/glass_image/frame.jpg")
                        conn.shutdown(SHUT_WR) # TODO instead of shutting down connection immediately, get the names with the help of Kairos and send them back
                elif request.startswith('CLOSE'):
                    print("Got close")
                    conn.shutdown(SHUT_WR)
            except:
                conn.shutdown(SHUT_WR)
                continue

        self.glassServerSocket.close()


    def startPhoneServer(self):
        print("startPhoneServer:")


    def analyzeFrame(self, image_path):
        print("Analyzing a frame from the client:")
        image_paths = glob.glob(os.path.join('image/glass_face/', "*"))
        face_count = len(image_paths)
        img = cv2.imread(image_path, 3)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 1:
            print("Error: " + str(len(faces)) + " detected!")
        else:
            print("Correct: 1 detected!")
            (x,y,w,h) = faces[0]
            crop_img = img[y:y+h, x:x+w]
            output_path = 'image/glass_face/' + str(face_count) + '.jpg'
            cv2.imwrite(output_path, crop_img)
            recognize_face_response = kairos_face.recognize_face(file=output_path, gallery_name='memento-test')
            print(recognize_face_response)
            print("Name detected: " + recognize_face_response['images'][0]['candidates'][0]['subject_id'] + '\n')
            


    def initKairos(self):
        kairos_face.remove_gallery(gallery_name="memento-test")
        image_paths = glob.glob(os.path.join('image/preset_image/', "*"))
        for image_path in image_paths:
            image_path = image_path.replace("\\", "/")
            file_name = image_path.split("/")[2]
            person_name = file_name.split(".")[0]
            img = cv2.imread(image_path, 3)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) != 1:
                print("Error: " + file_name + " " + str(len(faces)) + " detected!")
            else:
                print("Name: " + person_name)
                (x,y,w,h) = faces[0]
                crop_img = img[y:y+h, x:x+w]
                cv2.imwrite('image/preset_face/' + file_name, crop_img)
                enroll_face_response = kairos_face.enroll_face(file='image/preset_face/' + file_name, subject_id=person_name, gallery_name='memento-test')
                print(enroll_face_response)
                print("face_id: " + enroll_face_response['face_id'] + '\n')


server = Server()
#server.runServer()