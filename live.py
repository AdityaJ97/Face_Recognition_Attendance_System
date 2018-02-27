import face_recognition
import cv2

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
varad_image = face_recognition.load_image_file("./known/varad.jpg")
varad_face_encoding = face_recognition.face_encodings(varad_image)[0]

asa_image = face_recognition.load_image_file("./known/asa.jpg")
asa_face_encoding = face_recognition.face_encodings(asa_image)[0]

abhi_image = face_recognition.load_image_file("./known/abhi.jpg")
abhi_face_encoding = face_recognition.face_encodings(abhi_image)[0]

ameya_image = face_recognition.load_image_file("./known/ameya.jpg")
ameya_face_encoding = face_recognition.face_encodings(ameya_image)[0]

abhishek_image = face_recognition.load_image_file("./known/abhishek.jpg")
abhishek_face_encoding = face_recognition.face_encodings(abhishek_image)[0]

aditya_image = face_recognition.load_image_file("./known/aditya.jpg")
aditya_face_encoding = face_recognition.face_encodings(aditya_image)[0]



# Create arrays of known face encodings and their names
known_face_encodings = [
    varad_face_encoding,
    asa_face_encoding,
    abhi_face_encoding,
    ameya_face_encoding,
    abhishek_face_encoding,
    aditya_face_encoding
]
known_face_names = [
    "Varad",
    "Asawaree",
    "Abhishek",
    "Ameya",
    "Abhishek",
    "Aditya"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tolerance = 0.54
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
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            #matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding) 
	    name = "Unknown"
	    tempmin = 1
	    index = -1
	    for i, face_distance in enumerate(face_distances):
		if face_distance < tempmin:
			tempmin = face_distance
			index = i
            # If a match was found in known_face_encodings, just use the first one.
            #if True in matches:
            #    first_match_index = matches.index(True)
            #    name = known_face_names[first_match_index]
	    if tempmin < tolerance:
		name = known_face_names[index]
            face_names.append(name)
	    #print name

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
	cv2.namedWindow("Video", cv2.WND_PROP_FULLSCREEN)          
	cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, 1)
	cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
