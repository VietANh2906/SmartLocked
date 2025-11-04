from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, datetime, json

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

LOG_FILE = "logs.json"

# 10 locker demo
lockers = [{"id": i+1, "name": f"Locker {i+1}", "status": "open" if i % 2 == 0 else "closed"} for i in range(10)]

# Load logs
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = json.load(f)
else:
    logs = []

@app.route("/lockers")
def get_lockers():
    return jsonify(lockers)

@app.route("/logs")
def get_logs():
    return jsonify(logs)

@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files.get("file")
    locker_id = request.form.get("locker")
    if not file or not locker_id:
        return jsonify({"error": "Vui lòng chọn locker và file"}), 400

    filename = file.filename
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    locker = next((l for l in lockers if str(l["id"]) == locker_id), None)
    if locker:
        locker_name = locker["name"]
        locker["status"] = "closed"
    else:
        locker_name = "Unknown"

    log_entry = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "original_file": filename,
        "detected": "Detected",
        "faces": 1,
        "locker": locker_name
    }
    logs.append(log_entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "Upload thành công", "locker": locker_name})

@app.route("/clear-logs", methods=["DELETE"])
def clear_logs():
    global logs
    logs = []
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f)
    for locker in lockers:
        locker["status"] = "closed"
    return jsonify({"message": "Đã xóa logs và đóng tất cả locker"})

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
