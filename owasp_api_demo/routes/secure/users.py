"""Secure user endpoints."""

from fastapi import APIRouter, HTTPException, Depends, Request
from auth.dependencies import get_current_user
from database.mock_db import get_user_by_id, get_user_index_by_id, users_db
from models.request_models import ProfileUpdate
from utils.rate_limiting import check_rate_limit

router = APIRouter(prefix="/api/secure", tags=["secure-users"])

@router.get("/users/{user_id}")
async def get_user_secure(user_id: int, current_user: dict = Depends(get_current_user)):
    """SECURE: Proper authorization check"""
    # Check if user can access this resource
    if current_user["id"] != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return only safe data
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }

@router.get("/profile")
async def get_profile_secure(current_user: dict = Depends(get_current_user)):
    """SECURE: Property-level authorization"""
    user = get_user_by_id(current_user["id"])
    
    # Secure: Only return allowed properties
    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }

@router.put("/profile")
async def update_profile_secure(
    profile_data: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """SECURE: Controlled property updates"""
    user_index = get_user_index_by_id(current_user["id"])
    
    if user_index is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Secure: Only allow updating specific properties
    update_data = profile_data.dict(exclude_unset=True)
    
    # Remove role update for non-admin users
    if current_user["role"] != "admin" and "role" in update_data:
        del update_data["role"]
    
    users_db[user_index].update(update_data)
    
    return {"message": "Profile updated"}

@router.get("/data")
async def get_data_secure(request: Request, limit: int = 10):
    """SECURE: Rate limiting and resource bounds - API4:2023"""
    check_rate_limit(request, max_requests=100, window_minutes=15)
    
    # Secure: Bounded limit
    safe_limit = min(limit, 100)
    results = []
    
    for i in range(safe_limit):
        results.append({"id": i, "data": "Some data"})
    
    return results