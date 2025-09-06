"""Secure admin endpoints."""

from fastapi import APIRouter, Depends
from auth.dependencies import get_current_admin
from database.mock_db import delete_user_by_id, users_db, posts_db

router = APIRouter(prefix="/api/secure", tags=["secure-admin"])

@router.delete("/users/{user_id}")
async def delete_user_secure(user_id: int, current_user: dict = Depends(get_current_admin)):
    """SECURE: Proper function-level authorization"""
    delete_user_by_id(user_id)
    return {"message": "User deleted"}

@router.get("/admin/stats")
async def get_admin_stats_secure(current_user: dict = Depends(get_current_admin)):
    """SECURE: Role-based access"""
    return {
        "total_users": len(users_db),
        "total_posts": len(posts_db)
    }
