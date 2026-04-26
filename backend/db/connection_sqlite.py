"""
SQLite версия подключения к БД для разработки без Docker.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from db.models import Base
import os

# Используем SQLite для простоты
DATABASE_URL = "sqlite:///./answers.db"

# Создаем движок с поддержкой внешних ключей
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False  # Set to True for SQL debugging
)

# Включаем поддержку внешних ключей в SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

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
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized with SQLite")
    print(f"📁 Database file: {os.path.abspath('answers.db')}")


# Create tables on import
init_db()
