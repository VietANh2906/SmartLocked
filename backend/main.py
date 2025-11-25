from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import base64
import datetime

app = FastAPI(title="Smart Locker API")

# ===== CORS =====
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== DATA MOCK =====
lockers = [{"id": i+1, "name": f"Locker {i+1}", "status": "closed"} for i in range(8)]
logs = []

# ===== MODELS =====
class LogItem(BaseModel):
    id: int
    locker: int
    user: str
    time: str

# ===== ROUTES =====

@app.get("/lockers")
def get_lockers():
    return lockers

@app.get("/logs")
def get_logs():
    return logs

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    locker_id = (len(logs) % 8) + 1
    lockers[locker_id-1]["status"] = "open"

    log = {
        "id": len(logs)+1,
        "locker": locker_id,
        "user": file.filename,
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs.append(log)
    return {"success": True, "locker": locker_id, "logs": logs}

@app.post("/face/verify")
async def face_verify(b64: str = Form(...), locker_id: int = Form(...)):
    """
    Đây là giả lập nhận diện khuôn mặt
    """
    lockers[locker_id-1]["status"] = "open"

    log = {
        "id": len(logs)+1,
        "locker": locker_id,
        "user": f"FaceUser_{len(logs)+1}",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    logs.append(log)

    return {"success": True, "logs": logs}

@app.post("/close-locker/{locker_id}")
def close_locker(locker_id: int):
    for l in lockers:
        if l["id"] == locker_id:
            l["status"] = "closed"
    return {"locker_status": "closed"}

@app.delete("/clear-logs")
def clear_logs():
    logs.clear()
    for l in lockers:
        l["status"] = "closed"
    return {"success": True}
