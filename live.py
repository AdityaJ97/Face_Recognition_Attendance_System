import face_recognition
import cv2
import time
import datetime
from datetime import date
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",     
                     passwd="AbHiShEk",
                     db="FACE")
cur = db.cursor()

tt = {
"Sunday" : [],
"Monday" : [],
"Tuesday" : [],
"Wednesday" : [],
"Thursday" : [],
"Friday" : [],
"Saturday" : []
}

for i in range(8) :
	tt["Sunday"].append("SE")
	tt["Sunday"].append("OS")
	tt["Sunday"].append("AI")

tt["Monday"] = tt["Tuesday"] = tt["Wednesday"] = tt["Thursday"] = tt["Friday"] = tt["Saturday"] = tt["Sunday"]

video_capture = cv2.VideoCapture(0)

abhishek_image = face_recognition.load_image_file("./known/abhishek.jpg")
abhishek_face_encoding = face_recognition.face_encodings(abhishek_image)[0]

aditya_image = face_recognition.load_image_file("./known/aditya.jpg")
aditya_face_encoding = face_recognition.face_encodings(aditya_image)[0]

daivanti_image = face_recognition.load_image_file("./known/asa.jpg")
daivanti_face_encoding = face_recognition.face_encodings(daivanti_image)[0]

bala_image = face_recognition.load_image_file("./known/ameya.jpg")
bala_face_encoding = face_recognition.face_encodings(bala_image)[0]

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

hrs = {
        "111503027" : 0,
        "111503002" : 0,
        "111503012" : 0,
        "111508000" : 0
}

process_this_frame = True
while True:
    ret, frame = video_capture.read()

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1]

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
	mis = []

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.5)
            name = "Unknown"
	    misone = ""
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
		misone = mis_list[first_match_index]
            face_names.append(name)
	    mis.append(misone)

    process_this_frame = not process_this_frame

    for (top, right, bottom, left), name, misone in zip(face_locations, face_names, mis):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
	tempt = time.time()
	month = int(datetime.datetime.fromtimestamp(tempt).strftime('%m'))
	day = int(datetime.datetime.fromtimestamp(tempt).strftime('%d'))
	hr = int(datetime.datetime.fromtimestamp(tempt).strftime('%H')) 
	mini = int(datetime.datetime.fromtimestamp(tempt).strftime('%M'))
	d = time.strftime("%A", time.gmtime(tempt))
	if mini > 50:
		hr += 1
	if name != "unknown" and misone != "":
		tempv = tempt - ts[misone]
		start = hrs[misone]
		print name, hr, mini, d
		if ts[misone] == 0 :
			ts[misone] = tempt
			hrs[misone] = hr
		elif tempt - ts[misone] > 10 :
			while tempv > 10:
				ts[misone] = 0
				print tt[d][start]
                		print "UPDATE " + tt[d][start] + "_" + str(month) + " SET `" + str(day) + "` = `" + str(day) +"` + 1 where mis= '" + misone + "'"
				cur.execute("UPDATE " + tt[d][start] +"_" + str(month) + " SET `" + str(day) + "` = `" + str(day) +"` + 1 where mis= '" + misone + "'")
				db.commit()
				tempv -= 10
				start += 1
		
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    	
#    cv2.imshow('Video', frame)
#    if cv2.waitKey(33) & 0xFF == ord('q'):
#        break

db.close()
video_capture.release()
cv2.destroyAllWindows()
