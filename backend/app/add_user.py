from models import db, User
from flask import Flask
import face_recognition
import pickle
import os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, "smartlocker.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def add_user(name, image_path):
    # Load ảnh user
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    if len(encodings) == 0:
        print("Không tìm thấy khuôn mặt trong ảnh!")
        return

    face_encoding = encodings[0]

    # Tạo user mới
    user = User(name=name, face_encoding=face_encoding)
    db.session.add(user)
    db.session.commit()
    print(f"Đã thêm user {name} thành công!")

if __name__ == "__main__":
    with app.app_context():
        name = input("Nhập tên user: ")
        image_path = input("Đường dẫn ảnh: ")
        add_user(name, image_path)
