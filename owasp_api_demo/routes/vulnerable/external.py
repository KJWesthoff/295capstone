"""Vulnerable external API endpoints - API7:2023 & API10:2023."""

import time
from fastapi import APIRouter, HTTPException
from models.request_models import URLFetchRequest
from database.mock_db import add_user, users_db
from auth.utils import hash_password
import httpx

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-external"])

@router.post("/fetch-url")
async def fetch_url_vulnerable(url_data: URLFetchRequest):
    """VULNERABLE: SSRF vulnerability - API7:2023"""
    try:
        # VULNERABLE: No URL validation
        async with httpx.AsyncClient() as client:
            response = await client.get(url_data.url)
            return {"data": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/external-data/{external_id}")
async def get_external_data_vulnerable(external_id: str):
    """VULNERABLE: Unsafe consumption of external API - API10:2023"""
    try:
        # VULNERABLE: No validation of external data
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://jsonplaceholder.typicode.com/users/{external_id}")
            user_data = response.json()
        
        # VULNERABLE: Directly using external data without validation
        new_user = {
            "id": len(users_db) + 1,
            "username": user_data.get("username"),
            "email": user_data.get("email"),
            "role": user_data.get("role", "admin"),  # VULNERABLE: Could be privilege escalation
            "password": hash_password(user_data.get("password", "default123"))
        }
        
        add_user(new_user)
        
        return {"message": "User created from external data", "user": new_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))