import face_recognition

def load_known_faces(users):
    known_encodings = [user.face_encoding for user in users]
    known_names = [user.name for user in users]
    return known_encodings, known_names

def recognize_face(upload_image_path, known_encodings, known_names):
    image = face_recognition.load_image_file(upload_image_path)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    results = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]
        results.append(name)
    return results
