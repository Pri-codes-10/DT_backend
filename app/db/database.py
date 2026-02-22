"""Database connection manager."""

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Optional, Generator
import logging

DATABASE_URL = "postgresql://postgres:user123@localhost:5432/Digital_Twin"  # Default database URL, can be overridden by config

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
            logger.info("Database initialized successfully")
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
    
    def health_check(self) -> bool:
        """Check database connectivity."""
        try:
            with self.session_scope() as session:
                session.execute("SELECT 1")
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
