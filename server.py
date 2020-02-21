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
import time

class Server(object):

    def __init__(self):
        print("Initializing:\n")
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        kairos_face.settings.app_id = "8af0a9da"
        kairos_face.settings.app_key = "e24042917823dd0e625ecb500f4f9e44"
        self.galleryName = "memento-test"
        self.initKairos()
        self.glassServerSocket = socket(AF_INET, SOCK_STREAM) # for handling request from google glass
        self.phoneServerSocket = socket(AF_INET, SOCK_STREAM) # for handling request from cell phone
        self.glassPort = 8088
        self.phonePort = 8089
    

    def runServer(self):
        glassServerThread = threading.Thread(target=Server.startGlassSocket, args=(self,))
        glassServerThread.start()
        #phoneServerThread = threading.Thread(target=Server.startPhoneSocket, args=(self,))
        #phoneServerThread.start()


    def startGlassSocket(self):
        print("Start Glass Socket:")
        
        self.glassServerSocket.setblocking(0)
        self.glassServerSocket.setsockopt(SOL_SOCKET, SO_KEEPALIVE, 1)
        self.glassServerSocket.bind(("127.0.0.1", self.glassPort))
        #self.glassServerSocket.bind((gethostbyname(gethostname()), self.glassPort))
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
                else:
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        request = data.decode()
                        if request.startswith('POST'):
                            print("Glass client " + str(s.getpeername()) + " HTTP POST spam request. Connection shut down.")
                            inputs.remove(s)
                            s.close()
                        elif request.startswith('SIZE'):
                            strings = request.split()
                            size = int(strings[1])
                            print("Glass client " + str(s.getpeername()) + " request: post an image of " + str(size) + "Bytes.")
                            s.sendall("GOT SIZE".encode())
                            if not os.path.exists('image/glass_image'):
                                os.mkdir('image/glass_image')
                            imageFile = open("image/glass_image/received.jpg", 'wb')
                            received_size = 0
                            while received_size != size:
                                data = s.recv(1024)
                                imageFile.write(data)
                                received_size += len(data)
                            print("Glass client " + str(s.getpeername()) + " request: image bytes.")
                            print("Got image\n")
                            imageFile.close()
                            s.sendall("GOT IMAGE".encode())
                            # call Kairos to get name
                            name = self.analyzeFrame("image/glass_image/received.jpg")
                            name = name.replace('_',' ')
                            s.sendall(name.encode())
                        elif request != "":
                            print("Glass client " + str(s.getpeername()) + " request unknown: " + request)
                            s.sendall("UNKNOWN REQUEST".encode())
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
                else:
                    s.setblocking(1)
                    try:
                        data = s.recv(1024)
                        request = data.decode()
                        if request.startswith('POST'):
                            print("Phone client " + str(s.getpeername()) + " HTTP POST spam request. Connection shut down.")
                            inputs.remove(s)
                            s.close()
                        elif request.startswith('NEW'):
                            print("Phone client " + str(s.getpeername()) + " request: get a new face")
                            imageFile = open("unknown.jpg", 'rb')
                            imageBytes = imageFile.read()
                            size = len(imageBytes)
                            imageFile.close()
                            s.sendall(("SIZE " + str(size)).encode())
                            s.sendall(imageBytes)
                        elif request != "":
                            print("Phone client " + str(s.getpeername()) + " request unknown: " + request)
                            s.sendall("UNKNOWN REQUEST".encode())
                        else:
                            print("Phone client " + str(s.getpeername()) + " shut down connection.")
                            inputs.remove(s)
                            s.close()
                    except Exception as e:
                        print(e)
                        inputs.remove(s)
                        s.close()

        self.phoneServerSocket.close()


    def analyzeFrame(self, image_path):
        print("Analyzing Frame:")
        if not os.path.exists('image/glass_face'):
            os.mkdir('image/glass_face')
        image_paths = glob.glob(os.path.join('image/glass_face/', "*"))
        face_count = len(image_paths)
        img = cv2.imread(image_path, 3)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) != 1:
            # zero or multiple faces detected
            print("Error: " + str(len(faces)) + " faces detected!\n")
            return "ZeroOrMultipleFaces"
        else:
            (x,y,w,h) = faces[0]
            crop_img = img[y:y+h, x:x+w]
            # write cropped face image
            output_path = 'image/glass_face/' + str(face_count) + '.jpg'
            cv2.imwrite(output_path, crop_img)
            # recognizing cropped face image
            print("Recognizing: ")
            recognize_face_response = kairos_face.recognize_face(file=output_path, gallery_name='MementoTeamPhotos')
            #print(recognize_face_response)
            if 'candidates' in recognize_face_response['images'][0].keys():
                # kairos knows the face
                subject_id = recognize_face_response['images'][0]['candidates'][0]['subject_id']
                print("Name detected: " + subject_id + '\n')
                return subject_id
            else:
                # kairos doesn't know the face
                return "Unknown"
            

    def initKairos(self):
        # clear current Kairos gallery
        get_galleries_response = kairos_face.get_galleries_names_list()
        if self.galleryName in get_galleries_response['gallery_ids']:
            kairos_face.remove_gallery(gallery_name=self.galleryName)
        # initialize gallery with preset images
        if not os.path.exists('image/preset_image'):
            raise Exception
        if not os.path.exists('image/preset_face'):
            os.mkdir('image/preset_face')
        image_paths = glob.glob(os.path.join('image/preset_image/', "*"))
        for image_path in image_paths:
            image_path = image_path.replace("\\", "/") # Windows compatible
            file_name = image_path.split("/")[2]
            person_name = file_name.split(".")[0]
            img = cv2.imread(image_path, 3)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) != 1:
                # zero or multiple faces detected
                print("Error: " + file_name + " " + str(len(faces)) + " faces detected!\n")
            else:
                (x,y,w,h) = faces[0]
                crop_img = img[y:y+h, x:x+w]
                # write cropped face image
                crop_img_path = 'image/preset_face/' + file_name
                cv2.imwrite(crop_img_path, crop_img)
                # enroll cropped face images (not preset images)
                print("Enrolling: " + crop_img_path + " => " + person_name + "\n")
                enroll_face_response = kairos_face.enroll_face(file='image/preset_face/' + file_name, subject_id=person_name, gallery_name='MementoTeamPhotos')
                #print(enroll_face_response)
                face_id = enroll_face_response['face_id']
                #print("face_id: " + face_id + "\n")
        

server = Server()
server.runServer()
