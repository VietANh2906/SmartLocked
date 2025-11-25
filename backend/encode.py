import face_recognition
import cv2
import json

def encode_face_from_file(image_path):
    img = cv2.imread(image_path)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    
    if len(encodings) == 0:
        print("Không tìm thấy mặt trong ảnh!")
        return None
    
    return encodings[0].tolist()  # luôn 128 chiều

# Lấy encoding và lưu vào users.json
name = input("Tên người dùng: ")
locker = int(input("Số locker: "))
path = input("Đường dẫn ảnh: ")

encoding = encode_face_from_file(path)

if encoding is not None:
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

    users.append({
        "name": name,
        "locker": locker,
        "encoding": encoding
    })

    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    
    print(f"✅ Đã lưu {name} với encoding 128 chiều chuẩn")
