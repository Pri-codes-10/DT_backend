"""Main application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.config import config
from app.db.database import db_manager
from app.db.models import Base
from app.models import user  # Ensure models are imported
from app.utils.helpers import setup_logging
from app.routes import auth

# Setup logging
setup_logging(config.LOG_FILE, config.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""

    # ------------------- STARTUP -------------------
    logger.info(f"Starting {config.APP_NAME}...")

    # Ensure database URL comes from environment (Render safe)
    db_manager.database_url = config.DATABASE_URL

    # Initialize DB engine + pool
    db_manager.init_db()

    # ⚠️ Only use this in development
    if config.DEBUG and db_manager.engine:
        Base.metadata.create_all(bind=db_manager.engine)
        logger.info("Database tables created / verified")

    yield

    # ------------------- SHUTDOWN -------------------
    logger.info(f"Shutting down {config.APP_NAME}...")
    db_manager.close_db()


# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version="1.0.0",
    description="Backend service for digital twin health monitoring with LoRA fine-tuned models",
    lifespan=lifespan,
)

# Include auth router
app.include_router(auth.router)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "Digital Twin Health Backend API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    db_health = db_manager.health_check()
    return {
        "status": "healthy" if db_health else "unhealthy",
        "database": "connected" if db_health else "disconnected",
    }