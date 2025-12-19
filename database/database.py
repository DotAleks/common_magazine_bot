from typing import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
   create_async_engine,
   async_sessionmaker,
   AsyncSession
)

from database.models.base import Base
from core.logger import logger


class Database:
   """Manages database connections and operations using SQLAlchemy async.
    
   Attributes:
      engine: SQLAlchemy async engine instance
      asyncSession: Session factory for creating database sessions
    
   Args:
      db_url: Database connection URL
        
   Example:
      >>> db = Database("sqlite+aiosqlite:///./test.db")
      >>> await db.create_all_tables()
   """
   def __init__(self, db_url: str):
      self.engine = create_async_engine(db_url)
      self.async_session_factory = async_sessionmaker(
         self.engine,
         class_=AsyncSession,
         expire_on_commit=False,
         autoflush=False
      )
   @asynccontextmanager
   async def get_session(self) -> AsyncIterator[AsyncSession]:
      """Context manager for async database sessions with auto commit/rollback."""
      async with self.async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception as error:
           await session.rollback()
           logger.error(f"Database session error: {error}")
           raise
         
   async def create_all_tables(self) -> None:
      """Create all database tables from models."""
      try:
         async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
         logger.info("All database tables created successfully")
      except Exception as error:
         logger.error(f"Failed to create tables: {error}", exc_info=True)
         raise
   
   async def drop_all_tables(self) -> None:
      """Drop all database tables (warning: deletes all data)."""
      logger.warning("DROPPING ALL DATABASE TABLES - THIS WILL DELETE ALL DATA!")
      try:
         async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
         logger.warning("All database tables dropped successfully")
      except Exception as error:
         logger.error(f"Failed to drop tables: {error}", exc_info=True)
         raise

