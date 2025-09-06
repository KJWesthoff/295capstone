"""API Documentation endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["documentation"])

@router.get("/docs")
async def get_api_docs():
    """API Documentation"""
    return {
        "title": "OWASP API Security Top 10 Demo",
        "description": "Educational API demonstrating common vulnerabilities and secure implementations",
        "vulnerabilities": {
            "API1:2023": "Broken Object Level Authorization",
            "API2:2023": "Broken Authentication", 
            "API3:2023": "Broken Object Property Level Authorization",
            "API4:2023": "Unrestricted Resource Consumption",
            "API5:2023": "Broken Function Level Authorization",
            "API6:2023": "Unrestricted Access to Sensitive Business Flows",
            "API7:2023": "Server Side Request Forgery",
            "API8:2023": "Security Misconfiguration",
            "API9:2023": "Improper Inventory Management",
            "API10:2023": "Unsafe Consumption of APIs"
        },
        "endpoints": {
            "vulnerable": [
                "GET /api/vulnerable/users/{user_id}",
                "POST /api/vulnerable/login",
                "GET /api/vulnerable/profile", 
                "PUT /api/vulnerable/profile",
                "GET /api/vulnerable/data",
                "DELETE /api/vulnerable/users/{user_id}",
                "GET /api/vulnerable/admin/stats",
                "POST /api/vulnerable/transfer",
                "POST /api/vulnerable/fetch-url",
                "GET /api/vulnerable/config",
                "GET /api/vulnerable/debug",
                "GET /api/v1/internal/backup",
                "GET /api/v1/legacy/user-data",
                "GET /api/vulnerable/external-data/{external_id}"
            ],
            "secure": [
                "GET /api/secure/users/{user_id}",
                "POST /api/secure/login",
                "GET /api/secure/profile",
                "PUT /api/secure/profile", 
                "GET /api/secure/data",
                "DELETE /api/secure/users/{user_id}",
                "GET /api/secure/admin/stats",
                "POST /api/secure/transfer",
                "POST /api/secure/fetch-url",
                "GET /api/secure/health",
                "GET /api/v2/users/{user_id}",
                "GET /api/secure/external-data/{external_id}"
            ]
        },
        "authentication": {
            "vulnerable_login": {
                "endpoint": "POST /api/vulnerable/login",
                "credentials": {
                    "admin": {"username": "admin", "password": "admin123"},
                    "user1": {"username": "user1", "password": "password"},
                    "user2": {"username": "user2", "password": "secret"}
                }
            },
            "secure_login": {
                "endpoint": "POST /api/secure/login", 
                "note": "Use the same credentials but with proper bcrypt verification"
            }
        },
        "usage": {
            "install_dependencies": "pip install -r requirements.txt",
            "run_server": "uvicorn main:app --reload",
            "access_docs": "Visit http://localhost:8000/docs for interactive API documentation"
        }
    }