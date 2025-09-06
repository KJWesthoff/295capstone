"""Vulnerable admin endpoints - API5:2023 Broken Function Level Authorization."""

import time
from fastapi import APIRouter, HTTPException, Depends
from auth.dependencies import get_current_user
from database.mock_db import delete_user_by_id, users_db, posts_db

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-admin"])

@router.delete("/users/{user_id}")
async def delete_user_vulnerable(user_id: int, current_user: dict = Depends(get_current_user)):
    """VULNERABLE: Missing authorization check - API5:2023"""
    # VULNERABLE: Any authenticated user can delete any user
    delete_user_by_id(user_id)
    return {"message": "User deleted"}

@router.get("/admin/stats")
async def get_admin_stats_vulnerable(current_user: dict = Depends(get_current_user)):
    """VULNERABLE: Admin function without proper role check - API5:2023"""
    # VULNERABLE: No role verification
    return {
        "total_users": len(users_db),
        "total_posts": len(posts_db),
        "system_info": {
            "python_version": "3.9+",
            "uptime": time.time()
        }
    }

@router.get("/data")
async def get_data_vulnerable(limit: int = 1000000):
    """VULNERABLE: No rate limiting or resource bounds - API4:2023"""
    results = []
    
    # VULNERABLE: Can cause memory exhaustion
    for i in range(limit):
        results.append({"id": i, "data": "Some data " * 100})
    
    return results