"""Mock database for the OWASP API Security Demo."""

import bcrypt
from collections import defaultdict

# Mock database
users_db = [
    {
        "id": 1,
        "username": "admin",
        "password": bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()),
        "role": "admin",
        "email": "admin@example.com"
    },
    {
        "id": 2,
        "username": "user1",
        "password": bcrypt.hashpw("password".encode(), bcrypt.gensalt()),
        "role": "user",
        "email": "user1@example.com"
    },
    {
        "id": 3,
        "username": "user2",
        "password": bcrypt.hashpw("secret".encode(), bcrypt.gensalt()),
        "role": "user",
        "email": "user2@example.com"
    }
]

posts_db = [
    {"id": 1, "title": "Public Post", "content": "This is public", "author_id": 1, "is_private": False},
    {"id": 2, "title": "Private Post", "content": "This is private", "author_id": 2, "is_private": True},
    {"id": 3, "title": "Admin Post", "content": "Admin only", "author_id": 1, "is_private": True}
]

# Rate limiting storage
rate_limit_storage = defaultdict(list)
transfer_attempts = defaultdict(list)

def get_user_by_id(user_id: int):
    """Get user by ID."""
    return next((u for u in users_db if u["id"] == user_id), None)

def get_user_by_username(username: str):
    """Get user by username."""
    return next((u for u in users_db if u["username"] == username), None)

def get_user_index_by_id(user_id: int):
    """Get user index by ID."""
    return next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)

def delete_user_by_id(user_id: int):
    """Delete user by ID."""
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]

def add_user(user_data: dict):
    """Add a new user."""
    users_db.append(user_data)