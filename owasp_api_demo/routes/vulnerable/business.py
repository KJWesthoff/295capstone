"""Vulnerable business flow endpoints - API6:2023."""

import random
from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from models.request_models import TransferRequest

router = APIRouter(prefix="/api/vulnerable", tags=["vulnerable-business"])

@router.post("/transfer")
async def transfer_vulnerable(transfer_data: TransferRequest, current_user: dict = Depends(get_current_user)):
    """VULNERABLE: No protection against automated abuse - API6:2023"""
    # VULNERABLE: No rate limiting, no verification, no fraud detection
    transaction_id = f"tx_{random.randint(100000, 999999)}"
    
    return {
        "message": f"Transferred ${transfer_data.amount} to user {transfer_data.to_user_id}",
        "transaction_id": transaction_id
    }