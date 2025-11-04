import os
import requests
from PIL import Image, ImageDraw

# URL Flask API
url = "http://127.0.0.1:5000/detect"

# Thư mục chứa ảnh
image_dir = r"C:\Users\Acer\smart-locker\backend\known_faces"

# Duyệt tất cả file trong thư mục
for filename in os.listdir(image_dir):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(image_dir, filename)
        print(f"\n--- Xử lý ảnh: {filename} ---")

        # Gửi POST request
        with open(image_path, "rb") as f:
            files = {"image": f}
            response = requests.post(url, files=files)
        
        data = response.json()
        print("Kết quả nhận diện:", data)

        # Mở ảnh và vẽ khung
        img = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(img)
        for face in data.get("faces", []):
            top, right, bottom, left = face["location"]
            name = face["name"]
            draw.rectangle([left, top, right, bottom], outline="red", width=3)
            draw.text((left, bottom + 5), name, fill="red")
        
        # Hiển thị ảnh
        img.show()

        # Đổi tên file theo khuôn mặt (lấy khuôn mặt đầu tiên nếu có)
        if data.get("faces"):
            new_name = data["faces"][0]["name"] + os.path.splitext(filename)[1]
            new_path = os.path.join(image_dir, new_name)
            os.rename(image_path, new_path)
            print(f"Đã đổi tên file thành: {new_name}")
