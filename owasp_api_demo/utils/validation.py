"""Validation utilities."""

import re
from urllib.parse import urlparse
from fastapi import HTTPException
from config.settings import ALLOWED_DOMAINS

def validate_url(url: str, allowed_domains: list = None) -> bool:
    """Validate URL for SSRF protection."""
    if allowed_domains is None:
        allowed_domains = ALLOWED_DOMAINS
    
    try:
        parsed_url = urlparse(url)
        
        # Only allow HTTPS
        if parsed_url.scheme != "https":
            raise HTTPException(status_code=400, detail="Only HTTPS URLs allowed")
        
        # Check allowed domains
        if parsed_url.hostname not in allowed_domains:
            raise HTTPException(status_code=400, detail="Domain not allowed")
        
        return True
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid URL")

def validate_external_id(external_id: str, max_value: int = 10) -> bool:
    """Validate external ID."""
    if not re.match(r'^\d+$', external_id) or int(external_id) > max_value:
        raise HTTPException(status_code=400, detail="Invalid external ID")
    return True

def sanitize_username(username: str, max_length: int = 50) -> str:
    """Sanitize username input."""
    if not username:
        return f"user_{int(time.time())}"
    
    # Truncate and validate
    username = username[:max_length]
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return f"user_{int(time.time())}"
    
    return username

def sanitize_email(email: str, max_length: int = 100) -> str:
    """Sanitize email input."""
    if not email:
        return "noemail@example.com"
    
    email = email[:max_length]
    if "@" not in email:
        return "invalid@example.com"
    
    return email