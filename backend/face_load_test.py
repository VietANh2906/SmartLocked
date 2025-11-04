import face_recognition
import os

# 📁 Thư mục chứa ảnh nhận diện
KNOWN_FACES_DIR = "known_faces"

known_faces = []
known_names = []

# 🔄 Duyệt qua tất cả ảnh trong thư mục
for name in os.listdir(KNOWN_FACES_DIR):
    filepath = os.path.join(KNOWN_FACES_DIR, name)
    image = face_recognition.load_image_file(filepath)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) > 0:
        known_faces.append(encodings[0])
        known_names.append(os.path.splitext(name)[0])
        print(f"✅ Loaded {name}")
    else:
        print(f"⚠️ Không tìm thấy khuôn mặt trong {name}")

print("📸 Tổng số khuôn mặt đã nạp:", len(known_faces))
print("👤 Danh sách tên:", known_names)
