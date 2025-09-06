# OWASP API Security Top 10 Demo

An educational FastAPI application demonstrating the OWASP API Security Top 10 vulnerabilities and their secure implementations.

## Project Structure

```
owasp_api_demo/
├── main.py                     # FastAPI app initialization and main routes
├── requirements.txt            # Dependencies
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration settings
├── models/
│   ├── __init__.py
│   └── request_models.py      # Request/response models
├── database/
│   ├── __init__.py
│   └── mock_db.py             # Mock database
├── auth/
│   ├── __init__.py
│   ├── dependencies.py        # Authentication dependencies
│   └── utils.py               # Auth utility functions
├── routes/
│   ├── __init__.py
│   ├── vulnerable/            # Vulnerable endpoint implementations
│   │   ├── __init__.py
│   │   ├── auth.py            # API2:2023 - Broken Authentication
│   │   ├── users.py           # API1:2023 & API3:2023 - BOLA & Property Auth
│   │   ├── admin.py           # API4:2023 & API5:2023 - Resource & Function Auth
│   │   ├── business.py        # API6:2023 - Business Flows
│   │   ├── external.py        # API7:2023 & API10:2023 - SSRF & Unsafe Consumption
│   │   └── config.py          # API8:2023 & API9:2023 - Misconfiguration & Inventory
│   ├── secure/                # Secure endpoint implementations
│   │   ├── __init__.py
│   │   ├── auth.py            # Secure authentication
│   │   ├── users.py           # Secure user endpoints
│   │   ├── admin.py           # Secure admin endpoints
│   │   ├── business.py        # Secure business logic
│   │   ├── external.py        # Secure external API consumption
│   │   └── health.py          # Health check endpoints
│   └── docs.py                # Documentation endpoints
├── utils/
│   ├── __init__.py
│   ├── rate_limiting.py       # Rate limiting utilities
│   └── validation.py          # Validation utilities
└── middleware/
    ├── __init__.py
    └── cors.py                # CORS middleware
```

## OWASP API Security Top 10 Coverage

| Vulnerability | Vulnerable Endpoint | Secure Endpoint | Description |
|---------------|-------------------|-----------------|-------------|
| **API1:2023** | `GET /api/vulnerable/users/{user_id}` | `GET /api/secure/users/{user_id}` | Broken Object Level Authorization |
| **API2:2023** | `POST /api/vulnerable/login` | `POST /api/secure/login` | Broken Authentication |
| **API3:2023** | `GET/PUT /api/vulnerable/profile` | `GET/PUT /api/secure/profile` | Broken Object Property Level Authorization |
| **API4:2023** | `GET /api/vulnerable/data` | `GET /api/secure/data` | Unrestricted Resource Consumption |
| **API5:2023** | `DELETE /api/vulnerable/users/{user_id}` | `DELETE /api/secure/users/{user_id}` | Broken Function Level Authorization |
| **API6:2023** | `POST /api/vulnerable/transfer` | `POST /api/secure/transfer` | Unrestricted Access to Sensitive Business Flows |
| **API7:2023** | `POST /api/vulnerable/fetch-url` | `POST /api/secure/fetch-url` | Server Side Request Forgery |
| **API8:2023** | `GET /api/vulnerable/config` | `GET /api/secure/health` | Security Misconfiguration |
| **API9:2023** | `GET /api/v1/internal/backup` | `GET /api/v2/users/{user_id}` | Improper Inventory Management |
| **API10:2023** | `GET /api/vulnerable/external-data/{id}` | `GET /api/secure/external-data/{id}` | Unsafe Consumption of APIs |

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
uvicorn main:app --reload
```

The application will be available at:
- **Main API**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **API Documentation**: http://localhost:8000/api/docs

## Authentication

### Test Credentials

For both vulnerable and secure endpoints:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | admin |
| user1 | password | user |
| user2 | secret | user |

### Usage Example

1. **Login** (get JWT token):
   ```bash
   curl -X POST "http://localhost:8000/api/secure/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "admin", "password": "admin123"}'
   ```

2. **Use token** in subsequent requests:
   ```bash
   curl -X GET "http://localhost:8000/api/secure/profile" \
        -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

## Key Features

### Modular Architecture
- **Separation of Concerns**: Each component has a specific responsibility
- **Easy Maintenance**: Vulnerabilities and fixes are clearly separated
- **Scalable**: Easy to add new endpoints or modify existing ones

### Educational Value
- **Side-by-side Comparison**: Vulnerable vs secure implementations
- **Clear Documentation**: Each vulnerability is well-documented
- **Real-world Examples**: Practical security issues developers face

### Security Demonstrations
- **Authentication Flaws**: Weak vs strong password handling
- **Authorization Issues**: Missing vs proper access controls
- **Input Validation**: Unsafe vs validated data processing
- **Rate Limiting**: Unprotected vs protected endpoints
- **Configuration Security**: Exposed vs secured sensitive data

## Development Notes

### Adding New Endpoints

1. **Vulnerable Endpoint**: Add to appropriate file in `routes/vulnerable/`
2. **Secure Endpoint**: Add corresponding secure version in `routes/secure/`
3. **Update Documentation**: Add to `routes/docs.py`
4. **Register Router**: Include in `main.py`

### Configuration

All configuration is centralized in `config/settings.py`:
- JWT settings
- Rate limiting parameters
- External API configurations
- CORS settings

### Database

Uses a simple in-memory mock database in `database/mock_db.py`. In a real application, this would be replaced with actual database connections.

## Security Warnings

**This is an educational application demonstrating security vulnerabilities. Do not deploy to production or expose to the internet.**

The vulnerable endpoints intentionally contain security flaws for educational purposes. Always use the secure implementations as reference for production code.

## License

This project is for educational purposes. Please refer to OWASP guidelines for security best practices.