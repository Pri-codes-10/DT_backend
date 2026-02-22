"""User database model."""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.models import Base   # ✅ correct import


class User(Base):
    """User table model."""

    __tablename__ = "users"      # ✅ keep consistent with auth queries

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)

    email = Column(String(255), unique=True, nullable=False, index=True)

    # Support both local (hashed_password) and Google (google_id) authentication
    hashed_password = Column(String(255), nullable=True)  # nullable for Google login users
    google_id = Column(String(255), unique=True, nullable=True, index=True)  # Google OAuth ID
    login_provider = Column(String(50), default="local")  # "local" or "google"

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow   # ✅ auto timestamp
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"email={self.email}, "
            f"name={self.name})>"
        )
