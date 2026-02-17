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
        "postgresql://user:password@localhost:5432/digital_twin_health"
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
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # JWT (if using authentication)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_HOURS = 24


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./digital_twin_health_dev.db"
    )


class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False


def get_config() -> Config:
    """Get configuration based on environment."""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


# Global config instance
config = get_config()
