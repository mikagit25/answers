"""
Упрощенная версия подключения к БД для тестирования без Docker.
Использует SQLite вместо PostgreSQL.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
import os

# Используем SQLite для простоты тестирования
DATABASE_URL = "sqlite:///./answers_test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized with SQLite")


# Create tables immediately
init_db()
