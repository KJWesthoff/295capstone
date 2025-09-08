"""Main FastAPI application for OWASP API Security Top 10 Demo."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import (
    APP_TITLE, APP_VERSION, CORS_ORIGINS, CORS_CREDENTIALS, 
    CORS_METHODS, CORS_HEADERS
)

# Import routers
from routes.vulnerable import auth as vulnerable_auth
from routes.vulnerable import users as vulnerable_users
from routes.vulnerable import admin as vulnerable_admin
from routes.vulnerable import business as vulnerable_business
from routes.vulnerable import external as vulnerable_external
from routes.vulnerable import config as vulnerable_config

from routes.secure import auth as secure_auth
from routes.secure import users as secure_users
from routes.secure import admin as secure_admin
from routes.secure import business as secure_business
from routes.secure import external as secure_external
from routes.secure import health as secure_health

from routes import docs

# Create FastAPI app
app = FastAPI(title=APP_TITLE, version=APP_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

# Include vulnerable routers
app.include_router(vulnerable_auth.router)
app.include_router(vulnerable_users.router)
app.include_router(vulnerable_admin.router)
app.include_router(vulnerable_business.router)
app.include_router(vulnerable_external.router)
app.include_router(vulnerable_config.router)

# Include secure routers
app.include_router(secure_auth.router)
app.include_router(secure_users.router)
app.include_router(secure_admin.router)
app.include_router(secure_business.router)
app.include_router(secure_external.router)
app.include_router(secure_health.router)

# Include documentation router
app.include_router(docs.router)

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "OWASP API Security Top 10 Demo",
        "version": APP_VERSION,
        "documentation": {
            "api_docs": "/api/docs",
            "interactive_docs": "/docs",
            "openapi_schema": "/openapi.json"
        },
        "note": "This is an educational API demonstrating security vulnerabilities. Party On Dude."
    }

if __name__ == "__main__":
    import uvicorn
    print("OWASP API Security Top 10 Demo running on port 8000")
    print("Visit http://localhost:8000/api/docs for documentation")
    print("Visit http://localhost:8000/docs for interactive API documentation")
    uvicorn.run(app, host="0.0.0.0", port=8000)