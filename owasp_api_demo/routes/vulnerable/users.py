"""Vulnerable user endpoints - API1:2023 & API3:2023."""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from auth.dependencies import get_current_user
from database.mock_db import get_user_by_id, get_user_index_by_id, users_db

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-users"])

@router.get("/users/{user_id}")
async def get_user_vulnerable(user_id: int):
    """VULNERABLE: Direct object access without proper authorization - API1:2023"""
    user = get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # VULNERABLE: Returns sensitive data without checking authorization
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "password": user["password"].decode()  # VULNERABLE: Exposing password hash
    }

@router.get("/profile")
async def get_profile_vulnerable(current_user: dict = Depends(get_current_user)):
    """VULNERABLE: Exposes all object properties - API3:2023"""
    user = get_user_by_id(current_user["id"])
    
    # VULNERABLE: Returns all properties including sensitive ones
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "role": user["role"],
        "password": user["password"].decode()  # VULNERABLE: Password exposure
    }

@router.put("/profile")
async def update_profile_vulnerable(
    profile_data: Dict[str, Any], 
    current_user: dict = Depends(get_current_user)
):
    """VULNERABLE: Mass assignment - API3:2023"""
    user_index = get_user_index_by_id(current_user["id"])
    
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # VULNERABLE: Allows updating any property
    users_db[user_index].update(profile_data)
    
    return {"message": "Profile updated", "user": users_db[user_index]}