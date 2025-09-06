"""Rate limiting utilities."""

import time
from fastapi import HTTPException, Request, status
from database.mock_db import rate_limit_storage, transfer_attempts

def check_rate_limit(request: Request, max_requests: int = 100, window_minutes: int = 15):
    """Check if the request exceeds rate limits."""
    client_ip = request.client.host
    current_time = time.time()
    window_start = current_time - (window_minutes * 60)
    
    # Clean old requests
    rate_limit_storage[client_ip] = [
        req_time for req_time in rate_limit_storage[client_ip]
        if req_time > window_start
    ]
    
    if len(rate_limit_storage[client_ip]) >= max_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests from this IP"
        )
    
    rate_limit_storage[client_ip].append(current_time)

def check_transfer_rate_limit(request: Request, max_transfers: int = 5, window_hours: int = 1):
    """Check transfer rate limits."""
    client_ip = request.client.host
    current_time = time.time()
    window_start = current_time - (window_hours * 3600)
    
    # Clean old transfer attempts
    transfer_attempts[client_ip] = [
        attempt_time for attempt_time in transfer_attempts[client_ip]
        if attempt_time > window_start
    ]
    
    # Rate limit: transfers per hour
    if len(transfer_attempts[client_ip]) >= max_transfers:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many transfer attempts"
        )
    
    transfer_attempts[client_ip].append(current_time)