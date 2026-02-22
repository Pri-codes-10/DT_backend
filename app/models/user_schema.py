from pydantic import BaseModel, EmailStr
from typing import Optional

# Register request
class UserRegister(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str


# Login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Google login request
class GoogleLogin(BaseModel):
    token: str  # Google ID token from frontend


# Google user info (from Google OAuth)
class GoogleUserInfo(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None


# Response schema (optional but clean)
class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    login_provider: str

    class Config:
        from_attributes = True   # for SQLAlchemy → Pydantic


# Auth response with token
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse