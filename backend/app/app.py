from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mô phỏng trạng thái 10 locker
lockers = [{"id": i+1, "name": f"Locker {i+1}", "status": "closed"} for i in range(10)]
logs = []

@app.route("/lockers")
def get_lockers():
    return jsonify(lockers)

@app.route("/logs")
def get_logs():
    return jsonify(logs)

@app.route("/clear-logs", methods=["DELETE"])
def clear_logs():
    logs.clear()
    return jsonify({"message": "Logs cleared"}), 200

@app.route("/close-locker/<int:locker_id>", methods=["POST"])
def close_locker(locker_id):
    for locker in lockers:
        if locker["id"] == locker_id:
            locker["status"] = "closed"
    return jsonify({"locker_status": lockers})

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    locker_id = int(request.form.get("locker", 1))
    locker_name = f"Locker {locker_id}"

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Mô phỏng nhận diện thành công / thất bại
    import random
    success = random.choice([True, False])

    # Update locker nếu thành công
    for locker in lockers:
        if locker["id"] == locker_id:
            locker["status"] = "open" if success else "closed"

    logs.insert(0, {
        "id": locker_name,
        "locker": locker_name,
        "status": "Thành công" if success else "Thất bại",
        "thumbnail": filename if success else "-"
    })

    return jsonify({"locker_status": lockers, "log": logs[0]})

@app.route("/uploads/<filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
