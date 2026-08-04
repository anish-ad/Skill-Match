from pydantic import BaseModel, EmailStr, Field

class UserSignup(BaseModel):
    """Shape of data expected when a new user signs up."""
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    """Shape of data expected when a user logs in."""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Shape of user data we're safe to send back to the client (never the password!)."""
    id: str
    name: str
    email: EmailStr