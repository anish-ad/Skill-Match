from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import settings

def create_access_token(data: dict) -> str:
    """Generate a signed JWT containing the given data, with an expiry time."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    """Verify a JWT's signature and expiry. Returns the payload if valid, None if not."""
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None