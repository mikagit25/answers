from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid

Base = declarative_base()

class Tradition(Base):
    """Модель традиции (стоицизм, христианство и т.д.)"""
    __tablename__ = "traditions"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(10))
    color = Column(String(7))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    sources = relationship("Source", back_populates="tradition")
    
    def __repr__(self):
        return f"<Tradition(id='{self.id}', name='{self.name}')>"


class Source(Base):
    """Модель источника (цитата из первоисточника)"""
    __tablename__ = "sources"
    
    id = Column(String(100), primary_key=True)
    tradition_id = Column(String(50), ForeignKey("traditions.id"), nullable=False)
    author = Column(String(100), nullable=False)
    work = Column(String(200), nullable=False)
    section = Column(String(50))
    text = Column(Text, nullable=False)
    translation = Column(String(100))
    commentary = Column(Text)
    tags = Column(String(500))  # Comma-separated tags
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tradition = relationship("Tradition", back_populates="sources")
    chunks = relationship("Chunk", back_populates="source")
    
    def __repr__(self):
        return f"<Source(id='{self.id}', author='{self.author}')>"


class Chunk(Base):
    """Модель чанка для векторного поиска (фрагмент текста с эмбеддингом)"""
    __tablename__ = "chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(String(100), ForeignKey("sources.id"), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384))  # Dimension for paraphrase-multilingual-MiniLM
    metadata_json = Column(String(1000))  # Additional metadata as JSON string
    
    # Indexing
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    source = relationship("Source", back_populates="chunks")
    
    # Index for vector similarity search
    __table_args__ = (
        Index('idx_chunks_embedding', 'embedding', postgresql_using='ivfflat'),
    )
    
    def __repr__(self):
        return f"<Chunk(id='{self.id}', source_id='{self.source_id}')>"


class UserQuery(Base):
    """Модель пользовательского запроса (для истории и аналитики)"""
    __tablename__ = "user_queries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    tradition_id = Column(String(50), ForeignKey("traditions.id"))
    answer = Column(Text)
    session_id = Column(String(100))
    ip_hash = Column(String(64))  # Hashed IP for privacy
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer)
    cache_hit = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<UserQuery(id='{self.id}', question='{self.question[:50]}...')>"
