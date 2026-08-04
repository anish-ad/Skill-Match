from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from bson.errors import InvalidId

from app.core.jwt_handler import decode_access_token
from app.core.database import database

# Tells FastAPI where clients should send their token to get one
# (used mainly for the interactive /docs UI's "Authorize" button)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

users_collection = database["users"]


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Runs before any route that depends on it.
    Extracts and verifies the JWT from the Authorization header.
    Returns the authenticated user's data, or raises 401 if invalid.
    """
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