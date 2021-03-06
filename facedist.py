import face_recognition

known_abhishek_image = face_recognition.load_image_file("./known/abhishek.jpg")
known_aditya_image = face_recognition.load_image_file("./known/aditya.jpg")

abhishek_face_encoding = face_recognition.face_encodings(known_abhishek_image)[0]
aditya_face_encoding = face_recognition.face_encodings(known_aditya_image)[0]

known_encodings = [
    abhishek_face_encoding,
    aditya_face_encoding
]

image_to_test = face_recognition.load_image_file("./known/aj.jpeg")
image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]

face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)

for i, face_distance in enumerate(face_distances):
    print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
    print("- With a normal cutoff of 0.6, would the test image match the known image? {}".format(face_distance < 0.6))
    print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(face_distance < 0.5))
    print()
