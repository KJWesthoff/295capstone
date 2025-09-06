"""Secure authentication endpoints."""

from fastapi import APIRouter, HTTPException
from datetime import timedelta
from models.request_models import LoginRequest
from database.mock_db import get_user_by_username
from auth.utils import create_secure_access_token, verify_password

router = APIRouter(prefix="/api/secure", tags=["secure-auth"])

@router.post("/login")
async def login_secure(login_data: LoginRequest):
    """SECURE: Proper authentication"""
    if not login_data.username or not login_data.password:
        raise HTTPException(status_code=400, detail="Username and password required")
    
    user = get_user_by_username(login_data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Secure: Hash comparison
    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_secure_access_token(
        data={"id": user["id"], "username": user["username"], "role": user["role"]},
        expires_delta=timedelta(minutes=15)  # Secure: Short expiration
    )
    
    return {
        "token": token,
        "message": "Login successful",
        "user": {"id": user["id"], "username": user["username"], "role": user["role"]}
    }