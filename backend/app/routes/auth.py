from fastapi import APIRouter, HTTPException, status
from app.models.user import UserSignup, UserLogin, UserOut
from app.core.database import database
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token

router = APIRouter()
users_collection = database["users"]


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    # Check if a user with this email already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    # Hash the password before storing — never store plain text
    hashed_pw = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
    }

    result = await users_collection.insert_one(new_user)

    return UserOut(id=str(result.inserted_id), name=user.name, email=user.email)


@router.post("/login")
async def login(credentials: UserLogin):
    # Look up the user by email
    db_user = await users_collection.find_one({"email": credentials.email})
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Verify the provided password against the stored hash
    if not verify_password(credentials.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    # Credentials are valid — issue a JWT
    access_token = create_access_token(data={"sub": str(db_user["_id"])})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"],
        }
    }