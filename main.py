"""Main application entry point."""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.config import config
from app.db.database import db_manager
from app.utils.helpers import setup_logging
from app.routes import patients, predictions

# Setup logging
setup_logging(config.LOG_FILE, config.LOG_LEVEL)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {config.APP_NAME}...")
    db_manager.database_url = config.DATABASE_URL
    db_manager.init_db()
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {config.APP_NAME}...")
    db_manager.close_db()


# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME,
    version="1.0.0",
    description="Backend service for digital twin health monitoring with LoRA fine-tuned models",
    lifespan=lifespan,
)

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
    """Root endpoint."""
    return {
        "message": "Digital Twin Health Backend API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    db_health = db_manager.health_check()
    return {
        "status": "healthy" if db_health else "unhealthy",
        "database": "connected" if db_health else "disconnected",
    }


# Include route modules
# Uncomment when routes are fully implemented
# app.include_router(patients.router, prefix=f"/api/{config.API_VERSION}/patients", tags=["patients"])
# app.include_router(predictions.router, prefix=f"/api/{config.API_VERSION}/predictions", tags=["predictions"])


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=config.DEBUG,
        log_level=config.LOG_LEVEL.lower(),
    )
