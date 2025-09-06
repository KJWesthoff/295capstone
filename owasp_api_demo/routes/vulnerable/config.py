"""Vulnerable configuration endpoints - API8:2023 & API9:2023."""

import os
import time
from datetime import datetime
from fastapi import APIRouter
from config.settings import JWT_SECRET
from database.mock_db import users_db, posts_db

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-config"])

@router.get("/config")
async def get_config_vulnerable():
    """VULNERABLE: Exposes sensitive information - API8:2023"""
    # VULNERABLE: Exposes configuration details
    return {
        "database_url": "mongodb://admin:password@localhost:27017/mydb",
        "jwt_secret": JWT_SECRET,
        "api_keys": {
            "stripe": "sk_test_123456789",
            "sendgrid": "SG.abc123def456"
        },
        "debug": True,
        "environment": "production"
    }

@router.get("/debug")
async def get_debug_vulnerable():
    """VULNERABLE: Debug endpoint in production - API8:2023"""
    return {
        "environment": dict(os.environ),
        "users": users_db,  # VULNERABLE: Exposes all user data
        "uptime": time.time()
    }

# API9:2023 - Improper Inventory Management
@router.get("/v1/internal/backup")
async def get_backup_vulnerable():
    """VULNERABLE: Undocumented API endpoint - API9:2023"""
    # VULNERABLE: Undocumented endpoint that exposes data
    return {
        "users": users_db,
        "posts": posts_db,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/v1/legacy/user-data")
async def get_legacy_user_data(user_id: int):
    """VULNERABLE: Deprecated but still active endpoint - API9:2023"""
    from database.mock_db import get_user_by_id
    
    # VULNERABLE: Old endpoint with weak security
    user = get_user_by_id(user_id)
    
    if user:
        return user  # Returns all data including password hash
    else:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")