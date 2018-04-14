import face_recognition
import cv2
import time
import datetime
import MySQLdb

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="aditya123",  # your password
                     db="FACE")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
abhishek_image = face_recognition.load_image_file("./known/abhishek.jpg")
abhishek_face_encoding = face_recognition.face_encodings(abhishek_image)[0]

aditya_image = face_recognition.load_image_file("./known/aditya.jpg")
aditya_face_encoding = face_recognition.face_encodings(aditya_image)[0]

daivanti_image = face_recognition.load_image_file("./known/asa.jpg")
daivanti_face_encoding = face_recognition.face_encodings(daivanti_image)[0]

bala_image = face_recognition.load_image_file("./known/ameya.jpg")
bala_face_encoding = face_recognition.face_encodings(bala_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    abhishek_face_encoding,
    aditya_face_encoding,
    daivanti_face_encoding,
    bala_face_encoding
]
known_face_names = [
    "Abhishek Jadhav",
    "Aditya Jadhav",
    "Daivanti Thakare",
    "Bala"
]

mis_list = [
	"111503027",
	"111503002",
	"111507012",
	"111508000"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
mis = []
ts = {
	"111503027" : 0,
	"111503002" : 0,
	"111503012" : 0,
	"111508000" : 0
}
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
	mis = []

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.5)
            name = "Unknown"
	    misone = ""
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
		misone = mis_list[first_match_index]
            face_names.append(name)
	    mis.append(misone)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name, misone in zip(face_locations, face_names, mis):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
	tempt = time.time()
	month = int(datetime.datetime.fromtimestamp(tempt).strftime('%m'))
	day = int(datetime.datetime.fromtimestamp(tempt).strftime('%d'))
	if name != "unknown" and misone != "":
		if ts[misone] == 0 :
			ts[misone] = tempt
		elif tempt - ts[misone] > 10 :
			ts[misone] = tempt
			print "IN"
                	print "UPDATE SE_" + str(month) + " SET `" + str(day) + "` = `" + str(day) +"` + 1 where mis= '" + misone + "'"
			cur.execute("UPDATE SE_" + str(month) + " SET `" + str(day) + "` = `" + str(day) +"` + 1 where mis= '" + misone + "'")
			db.commit()
		
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
	#print "UPDATE attendance SET record = 1 where mis=" + misone
#	if name != "unknown":
		#cur.execute("UPDATE attendance SET record = 1 where mis= '" + misone + "'")
		#db.commit()
    	
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

db.close()
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
