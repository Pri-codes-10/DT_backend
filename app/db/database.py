"""Database connection manager."""
from sqlalchemy import text
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Optional, Generator
import logging
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://digital_twin_tw2q_user:rm8t1cQSo5kRlybpcZ4fnMiAgYKE4SsZ@dpg--a.singapore-postgres.render.com:5432/digital_twin_tw2q?sslmode=require")  # Default database URL, can be overridden by config

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""
    
    def __init__(self, database_url: str, pool_size: int = 10, max_overflow: int = 20):
        """
        Initialize database manager.
        
        Args:
            database_url: SQLAlchemy database URL
            pool_size: Connection pool size
            max_overflow: Max overflow connections
        """
        self.database_url = database_url
        self.engine: Optional[Engine] = None
        self.SessionLocal = None
        self.pool_size = pool_size
        self.max_overflow = max_overflow
    
    def init_db(self) -> None:
        """Initialize database connection and engine."""
        try:
            self.engine = create_engine(
                self.database_url,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                echo=False,
            )

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine,
            )

            # 🔥 FORCE TEST CONNECTION
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logger.info("Database initialized and connected successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session."""
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized. Call init_db() first.")
        return self.SessionLocal()
    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """Context manager for database sessions."""
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def close_db(self) -> None:
        """Close database connections."""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")
    
    from sqlalchemy import text

def health_check(self) -> bool:
    """Check database connectivity."""
    try:
        if not self.engine:
            return False

        with self.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True

    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# Global database manager instance
db_manager = DatabaseManager(DATABASE_URL)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency to get a database session."""
    session = db_manager.get_session()
    try:
        yield session
    finally:
        session.close()
