from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)  # Cho phép React truy cập
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔐 Danh sách 10 tủ khóa
lockers = [{"id": i, "name": f"Locker {i}", "status": "closed"} for i in range(1, 11)]
logs = []


@app.route("/lockers", methods=["GET"])
def get_lockers():
    return jsonify(lockers)


@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify(logs)


@app.route("/upload", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    locker_id = int(request.form.get("locker", 1))
    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)

    # ✅ Chỉ mở tủ được chọn — không đóng các tủ khác
    for l in lockers:
        if l["id"] == locker_id:
            l["status"] = "open"
            break

    # ✅ Ghi log mới
    logs.insert(
        0,
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "file": filename,
            "result": "Detected",
            "faces": 1,
            "locker": f"Locker {locker_id}",
        },
    )

    return jsonify({
        "message": f"Tải lên thành công: {filename}",
        "locker_status": lockers
    })


# ✅ API mới: Đóng riêng từng tủ
@app.route("/close-locker/<int:locker_id>", methods=["POST"])
def close_locker(locker_id):
    found = False
    for l in lockers:
        if l["id"] == locker_id:
            l["status"] = "closed"
            found = True
            break

    if not found:
        return jsonify({"error": "Locker not found"}), 404

    logs.insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": "",
        "result": "Locker closed",
        "faces": 0,
        "locker": f"Locker {locker_id}"
    })

    return jsonify({
        "message": f"Locker {locker_id} closed successfully",
        "locker_status": lockers
    })


@app.route("/clear-logs", methods=["DELETE"])
def clear_logs():
    logs.clear()
    for l in lockers:
        l["status"] = "closed"
    return jsonify({"message": "All logs cleared", "locker_status": lockers})


if __name__ == "__main__":
    app.run(debug=True)
