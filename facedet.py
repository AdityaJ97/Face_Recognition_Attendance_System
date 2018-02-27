import cv2
import numpy as np
import face_recognition

picture_of_me = face_recognition.load_image_file("./known/aditya.JPG")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cas = cv2.CascadeClassifier('haarcascade_eye.xml')
vid = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
while True:
	ret, img = vid.read()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
		cv2.putText(img, 'FACE HERE', (x, y-3), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)
		roi_gray = gray[y:y+h, x:x+w]
		roi_color = img[y:y+h, x:x+w]
		unknown_picture = roi_color
		unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# Now we can see the two face encodings are of the same person with `compare_faces`!

		results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

		if results[0] == True:
		    print("It's a picture of me!")
		else:
    			print("It's not a picture of me!")

		eyes = eye_cas.detectMultiScale(roi_gray)
		for(ex, ey, ew, eh) in eyes:
			cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
	cv2.imshow('img', img)
	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break
vid.release()
cv2.destroyAllWindows()

