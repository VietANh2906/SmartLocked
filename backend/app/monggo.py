# backend/app/monggo.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy URI từ .env
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not set in .env")

# Kết nối MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.smart_locker

# Các collection
users_collection = db.users
lockers_collection = db.lockers
logs_collection = db.logs
