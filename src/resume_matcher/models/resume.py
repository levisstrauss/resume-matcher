from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from ..core.database import Base
from ..core.config import settings


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    # User info
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)

    # Resume content
    filename = Column(String(255), nullable=False)
    raw_text = Column(Text, nullable=False)

    # Vector embedding for semantic search
    embedding = Column(Vector(settings.embedding_dimensions), nullable=True)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Resume(id={self.id}, name='{self.name}')>"