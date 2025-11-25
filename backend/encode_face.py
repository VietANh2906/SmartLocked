# encode_face.py
import face_recognition
import json
import sys
import os

USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return []

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def encode_face(image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        print("⚠️ Không tìm thấy mặt trong ảnh!")
        return None
    return encodings[0].tolist()  # luôn 128 chiều

def add_or_update_user(name, locker_id, image_path):
    encoding = encode_face(image_path)
    if encoding is None:
        return

    users = load_users()
    # Kiểm tra user đã tồn tại chưa
    found = False
    for user in users:
        if user["name"] == name:
            user["locker"] = locker_id
            user["encoding"] = encoding
            found = True
            print(f"✅ Cập nhật encoding cho {name} vào locker {locker_id}")
            break

    if not found:
        users.append({
            "name": name,
            "locker": locker_id,
            "encoding": encoding
        })
        print(f"✅ Thêm user {name} với locker {locker_id}")

    save_users(users)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Cách dùng: python encode_face.py <Tên User> <Locker ID> <Ảnh>")
        sys.exit(1)

    user_name = sys.argv[1]
    locker_id = int(sys.argv[2])
    image_file = sys.argv[3]

    add_or_update_user(user_name, locker_id, image_file)
