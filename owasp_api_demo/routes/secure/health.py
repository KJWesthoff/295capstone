"""Secure health and configuration endpoints."""

from fastapi import APIRouter
from datetime import datetime
from models.request_models import HealthResponse
from config.settings import APP_VERSION

router = APIRouter(prefix="/api/secure", tags=["secure-health"])

@router.get("/health", response_model=HealthResponse)
async def get_health_secure():
    """SECURE: Proper configuration management - API8:2023"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=APP_VERSION
    )