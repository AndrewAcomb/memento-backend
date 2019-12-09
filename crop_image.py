import cv2
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

img = cv2.imread("bryan_li.jpg", 3)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)

count = 0
for (x,y,w,h) in faces:

    crop_img = img[y:y+h, x:x+w]
    count += 1
    cv2.imwrite('cropped/' + str(count) + '.jpg', crop_img)
    
    cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0 , 0 ), 2)

    

cv2.imshow('frame', img)
cv2.imwrite('output.jpg', img)
cv2.waitKey(5000)
cv2.destroyAllWindows()

cv2.data.haarcascades