"""Vulnerable authentication endpoints - API2:2023 Broken Authentication."""

from fastapi import APIRouter, HTTPException
from datetime import timedelta
from models.request_models import LoginRequest
from database.mock_db import get_user_by_username
from auth.utils import create_access_token

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-auth"])

@router.post("/login")
async def login_vulnerable(login_data: LoginRequest):
    """VULNERABLE: Weak authentication"""
    user = get_user_by_username(login_data.username)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # VULNERABLE: Plain text password comparison
    if login_data.password in ["admin123", "password", "secret"]:
        token = create_access_token(
            data={"id": user["id"], "username": user["username"], "role": user["role"]},
            expires_delta=timedelta(days=365)  # VULNERABLE: Long expiration
        )
        
        return {
            "token": token,
            "message": "Login successful",
            "user": {"id": user["id"], "username": user["username"], "role": user["role"]}
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")