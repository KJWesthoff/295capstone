"""Configuration settings for the OWASP API Security Demo."""

import os
from datetime import timedelta

# JWT Settings
JWT_SECRET = "super-secret-key"  # VULNERABLE: Weak secret in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

# Rate Limiting Settings
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW_MINUTES = 15
TRANSFER_RATE_LIMIT = 5
TRANSFER_RATE_WINDOW_HOURS = 1

# API Settings
MAX_RESPONSE_SIZE = 1000
MAX_DATA_LIMIT = 100
MAX_TRANSFER_AMOUNT = 10000

# External API Settings
ALLOWED_DOMAINS = ["api.github.com", "jsonplaceholder.typicode.com"]
EXTERNAL_API_TIMEOUT = 5.0

# CORS Settings
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# App Settings
APP_TITLE = "OWASP API Security Top 10 Demo"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"