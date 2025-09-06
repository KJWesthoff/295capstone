"""Secure external API endpoints."""

import time
from fastapi import APIRouter, HTTPException, Depends
from auth.dependencies import get_current_user, get_current_admin
from models.request_models import URLFetchRequest
from database.mock_db import add_user, users_db
from auth.utils import hash_password
from utils.validation import validate_url, validate_external_id, sanitize_username, sanitize_email
from config.settings import EXTERNAL_API_TIMEOUT, MAX_RESPONSE_SIZE
import httpx

router = APIRouter(prefix="/api/secure", tags=["secure-external"])

@router.post("/fetch-url")
async def fetch_url_secure(url_data: URLFetchRequest, current_user: dict = Depends(get_current_user)):
    """SECURE: Protected against SSRF - API7:2023"""
    try:
        # Secure: URL validation
        validate_url(url_data.url)
        
        async with httpx.AsyncClient(timeout=EXTERNAL_API_TIMEOUT) as client:
            response = await client.get(url_data.url)
            # Limit response size
            limited_data = response.text[:MAX_RESPONSE_SIZE]
            return {"data": limited_data}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail="Fetch failed")

@router.get("/external-data/{external_id}")
async def get_external_data_secure(external_id: str, current_user: dict = Depends(get_current_admin)):
    """SECURE: Safe consumption of external APIs - API10:2023"""
    # Secure: Input validation
    validate_external_id(external_id, max_value=10)
    
    try:
        async with httpx.AsyncClient(timeout=EXTERNAL_API_TIMEOUT) as client:
            response = await client.get(
                f"https://jsonplaceholder.typicode.com/users/{external_id}",
                headers={"User-Agent": "SecureApp/1.0"}
            )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="External API error")
        
        user_data = response.json()
        
        # Secure: Validate and sanitize external data
        username = sanitize_username(user_data.get("username", f"user_{int(time.time())}"))
        email = sanitize_email(user_data.get("email", "noemail@example.com"))
        
        validated_user = {
            "id": len(users_db) + 1,
            "username": username,
            "email": email,
            "role": "user",  # Secure: Always assign safe default role
            "password": hash_password("changeMe123!")
        }
        
        add_user(validated_user)
        
        return {
            "message": "User created safely from external data",
            "user": {
                "id": validated_user["id"],
                "username": validated_user["username"],
                "email": validated_user["email"],
                "role": validated_user["role"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to process external data")

@router.get("/v2/users/{user_id}")
async def get_user_v2_secure(user_id: int, current_user: dict = Depends(get_current_user)):
    """SECURE: Properly documented and versioned endpoint - API9:2023"""
    from database.mock_db import get_user_by_id
    
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }