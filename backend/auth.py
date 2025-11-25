# backend/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.monggo import users_collection
from passlib.context import CryptContext
import jwt
import datetime
import os
from dotenv import load_dotenv
 

# Load .env
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

# Hash password
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    username: str
    password: str
    email: str

class LoginData(BaseModel):
    username: str
    password: str

# Register
@router.post("/register")
async def register(user: User):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    user_dict = {"username": user.username, "password": hashed_password, "email": user.email}
    await users_collection.insert_one(user_dict)
    return {"msg": "User registered successfully"}

# Login
@router.post("/login")
async def login(data: LoginData):
    user = await users_collection.find_one({"username": data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = jwt.encode(
        {"username": data.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token}


   if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not pwd_context.verify(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    token = jwt.encode(
        {"username": data.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
        SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token}
