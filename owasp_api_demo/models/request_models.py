"""Request and response models for the API."""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: Optional[str] = None

class ProfileUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None

class TransferRequest(BaseModel):
    to_user_id: int
    amount: float
    verification_code: Optional[str] = None

class URLFetchRequest(BaseModel):
    url: str

class ExternalDataRequest(BaseModel):
    external_id: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str