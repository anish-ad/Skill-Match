from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from bson import ObjectId
from bson.errors import InvalidId

from app.core.jwt_handler import decode_access_token
from app.core.database import database

# Simple "paste your bearer token" scheme — no username/password form
bearer_scheme = HTTPBearer()

users_collection = database["users"]


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """
    Runs before any route that depends on it.
    Extracts and verifies the JWT from the Authorization header.
    Returns the authenticated user's data, or raises 401 if invalid.
    """
    token = credentials.credentials  # the raw token string, after "Bearer "

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        raise credentials_exception

    if user is None:
        raise credentials_exception

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
    }