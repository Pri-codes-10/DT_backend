"""Application configuration."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration."""
    
    # App settings
    APP_NAME = "Digital Twin Health Backend"
    DEBUG = False
    TESTING = False
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://digital_twin_tw2q_user:rm8t1cQSo5kRlybpcZ4fnMiAgYKE4SsZ@dpg-d6esf35m5p6s73fs920g-a/digital_twin_tw2q"
    )
    
    # LoRA Model settings
    LORA_RANK = int(os.getenv("LORA_RANK", 8))
    LORA_ALPHA = int(os.getenv("LORA_ALPHA", 16))
    LORA_DROPOUT = float(os.getenv("LORA_DROPOUT", 0.1))
    MODEL_CHECKPOINT_PATH = os.getenv("MODEL_CHECKPOINT_PATH", "./models/checkpoints")
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", 8000))
    API_VERSION = "v1"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")
    
    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5174").split(",")
    
    # JWT (if using authentication)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://digital_twin_tw2q_user:rm8t1cQSo5kRlybpcZ4fnMiAgYKE4SsZ@dpg-d6esf35m5p6s73fs920g-a/digital_twin_tw2q"
    )


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DATABASE_URL = "postgresql://digital_twin_tw2q_user:rm8t1cQSo5kRlybpcZ4fnMiAgYKE4SsZ@dpg-d6esf35m5p6s73fs920g-a/digital_twin_tw2q"


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        cfg = ProductionConfig()
    elif env == "testing":
        cfg = TestingConfig()
    else:
        cfg = DevelopmentConfig()
    
    # enforce presence of DATABASE_URL in non-development environments
    if env in ("production", "testing") and not cfg.DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable must be set")
    return cfg


# Global config instance
config = get_config()
