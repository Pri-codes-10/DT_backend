"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables (for local dev only)
load_dotenv()


class Config:
    """Base configuration."""

    # App settings
    APP_NAME = "Digital Twin Health Backend"
    DEBUG = False
    TESTING = False

    # ---------------- DATABASE ----------------
    # MUST be provided via environment variable
    DATABASE_URL = os.getenv("DATABASE_URL")

    # ---------------- MODEL ----------------
    LORA_RANK = int(os.getenv("LORA_RANK", 8))
    LORA_ALPHA = int(os.getenv("LORA_ALPHA", 16))
    LORA_DROPOUT = float(os.getenv("LORA_DROPOUT", 0.1))
    MODEL_CHECKPOINT_PATH = os.getenv("MODEL_CHECKPOINT_PATH", "./models/checkpoints")

    # ---------------- API ----------------
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_VERSION = "v1"

    # ---------------- LOGGING ----------------
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")

    # ---------------- CORS ----------------
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5174"
    ).split(",")

    # ---------------- JWT ----------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24

    # ---------------- GOOGLE OAUTH ----------------
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


def get_config() -> Config:
    """Return config based on ENVIRONMENT variable."""

    env = os.getenv("ENVIRONMENT", "development").lower()

    if env == "production":
        cfg = ProductionConfig()
    elif env == "testing":
        cfg = TestingConfig()
    else:
        cfg = DevelopmentConfig()

    # 🚨 Enforce DATABASE_URL in production/testing
    if env in ("production", "testing") and not cfg.DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable must be set")

    return cfg


# Global config instance
config = get_config()