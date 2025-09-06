"""Secure business flow endpoints."""

import random
from fastapi import APIRouter, HTTPException, Depends, Request
from auth.dependencies import get_current_user
from models.request_models import TransferRequest
from utils.rate_limiting import check_transfer_rate_limit
from config.settings import MAX_TRANSFER_AMOUNT

router = APIRouter(prefix="/api/secure", tags=["secure-business"])

@router.post("/transfer")
async def transfer_secure(
    request: Request,
    transfer_data: TransferRequest,
    current_user: dict = Depends(get_current_user)
):
    """SECURE: Protected sensitive business flow - API6:2023"""
    # Rate limit: 5 transfers per hour
    check_transfer_rate_limit(request, max_transfers=5, window_hours=1)
    
    # Secure: Require verification
    if not transfer_data.verification_code:
        raise HTTPException(status_code=400, detail="Verification code required")
    
    # Secure: Amount limits
    if transfer_data.amount > MAX_TRANSFER_AMOUNT:
        raise HTTPException(status_code=400, detail="Amount exceeds daily limit")
    
    transaction_id = f"tx_{random.randint(100000, 999999)}"
    
    return {
        "message": f"Transfer of ${transfer_data.amount} initiated and requires approval",
        "transaction_id": transaction_id,
        "status": "pending_approval"
    }