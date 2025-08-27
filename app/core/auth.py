"""
Production Authentication for Configuration API
Secure authentication middleware for production configuration changes.
"""

import os
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

def get_admin_token() -> str:
    """Get the admin token from environment variables."""
    token = os.getenv("ADMIN_API_TOKEN")
    if not token:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_API_TOKEN not configured"
        )
    return token

def verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """Verify the admin token for configuration API access."""
    try:
        admin_token = get_admin_token()
        
        # Simple token comparison for basic auth
        if credentials.credentials == admin_token:
            return True
            
        # JWT token verification (if using JWT)
        try:
            jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
            payload = jwt.decode(
                credentials.credentials, 
                jwt_secret, 
                algorithms=["HS256"]
            )
            
            # Check if token has admin role
            if payload.get("role") == "admin":
                return True
                
        except jwt.InvalidTokenError:
            pass
            
        raise HTTPException(
            status_code=403,
            detail="Invalid admin token"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Authentication failed"
        )

def verify_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
    """Verify API key from header."""
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key required in X-API-Key header"
        )
    
    expected_key = os.getenv("CONFIG_API_KEY")
    if not expected_key:
        raise HTTPException(
            status_code=500,
            detail="CONFIG_API_KEY not configured"
        )
    
    # Secure comparison to prevent timing attacks
    if not hmac.compare_digest(x_api_key, expected_key):
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    
    return True

def create_admin_token(role: str = "admin") -> str:
    """Create a JWT token for admin access."""
    jwt_secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    
    payload = {
        "role": role,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    return jwt.encode(payload, jwt_secret, algorithm="HS256")
