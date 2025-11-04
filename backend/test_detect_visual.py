import requests
from PIL import Image, ImageDraw
import io

# URL API Flask của bạn
url = "http://127.0.0.1:5000/detect"

# Đường dẫn tới file ảnh muốn nhận diện
image_path = r"C:\Users\Acer\smart-locker\backend\known_faces\AnhHoang.jpg"

# Mở file và gửi POST request
with open(image_path, "rb") as f:
    files = {"image": f}
    response = requests.post(url, files=files)

# Nhận dữ liệu JSON
data = response.json()
print("Kết quả nhận diện khuôn mặt:")
print(data)

# Hiển thị ảnh và vẽ khung
img = Image.open(image_path).convert("RGB")
draw = ImageDraw.Draw(img)

for face in data.get("faces", []):
    top, right, bottom, left = face["location"]
    name = face["name"]
    # Vẽ khung chữ nhật quanh khuôn mặt
    draw.rectangle([left, top, right, bottom], outline="red", width=3)
    # Viết tên dưới khung
    draw.text((left, bottom + 5), name, fill="red")

# Hiển thị ảnh
img.show()
