from pymongo import MongoClient
import face_recognition
import os

UPLOAD_FOLDER = "uploads"

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["face_db"]
collection = db["logs"]

# Lấy tất cả log có locations rỗng
logs = collection.find({"locations": {"$size": 0}})

for log in logs:
    filename = log["filename"]
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        image = face_recognition.load_image_file(filepath)
        face_locations = face_recognition.face_locations(image)
        faces_data = [{"location": loc, "name": "unknown"} for loc in face_locations]

        # Cập nhật document
        collection.update_one(
            {"_id": log["_id"]},
            {"$set": {"locations": faces_data}}
        )
        print(f"Updated {filename} with {len(faces_data)} faces.")
    else:
        print(f"File {filename} not found, skipped.")
