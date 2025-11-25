from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ===============================
# 👤 Bảng Người dùng (User)
# ===============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    image_path = db.Column(db.String(255))  # đường dẫn ảnh khuôn mặt

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_path": self.image_path
        }

# ===============================
# 🔒 Bảng Locker
# ===============================
class Locker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), default="locked")  # "locked" hoặc "opened"
    last_opened = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "last_opened": self.last_opened.strftime("%Y-%m-%d %H:%M:%S") if self.last_opened else None
        }

# ===============================
# 🧾 Bảng Log
# ===============================
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50))
    filename = db.Column(db.String(255))
    detected_faces = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    locker_id = db.Column(db.Integer, db.ForeignKey("locker.id"))
    image_path = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "filename": self.filename,
            "detected_faces": self.detected_faces,
            "user_name": self.user_name,
            "locker_id": self.locker_id,
            "image_path": self.image_path
        }
