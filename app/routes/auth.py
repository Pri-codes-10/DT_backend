from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.user_schema import UserRegister, UserLogin, GoogleLogin, UserResponse
from app.utils.auth_utils import hash_password, verify_password
from app.utils.google_auth_utils import google_oauth

router = APIRouter(prefix="/auth", tags=["Auth"])


# REGISTER (LOCAL)
@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    # Check if email exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=hash_password(user.password),
        login_provider="local"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": UserResponse.from_orm(new_user)}


# LOGIN (LOCAL)
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if user registered with Google instead of password
    if db_user.login_provider == "google":
        raise HTTPException(
            status_code=400,
            detail="This account is registered with Google. Please use Google login."
        )

    if not db_user.hashed_password or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {
        "message": "Login successful",
        "user": UserResponse.from_orm(db_user)
    }


# GOOGLE LOGIN
@router.post("/google-login")
def google_login(request: GoogleLogin, db: Session = Depends(get_db)):
    """
    Authenticate user with Google OAuth token.
    
    Frontend should:
    1. Call Google Sign-In SDK
    2. Get the ID token
    3. Send token to this endpoint
    """

    if not google_oauth:
        raise HTTPException(
            status_code=500,
            detail="Google OAuth not configured"
        )

    # Verify the Google token
    google_user = google_oauth.verify_token(request.token)

    if not google_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google token"
        )

    # Check if user already exists
    db_user = db.query(User).filter(User.email == google_user['email']).first()

    if db_user:
        # User exists, check if they registered with Google
        if db_user.login_provider == "local":
            raise HTTPException(
                status_code=400,
                detail="This email is already registered with password login. "
                       "Please use your password to login or recover your account."
            )
        # Update Google ID if not already set
        if not db_user.google_id:
            db_user.google_id = google_user['google_id']
            db.commit()
    else:
        # Create new user with Google
        new_user = User(
            name=google_user['name'],
            surname=google_user['surname'],
            email=google_user['email'],
            google_id=google_user['google_id'],
            login_provider="google"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        db_user = new_user

    return {
        "message": "Google login successful",
        "user": UserResponse.from_orm(db_user)
    }
