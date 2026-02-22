import os
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base
from pgvector.sqlalchemy import Vector
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# 1536 is chosen based on Nomic v1.5 embed dimension, but we should verify.
# Nomic-embed-text-v1.5 has an embedding dimension of 768 by default.
EMBEDDING_DIM = 768

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://nyu:password@127.0.0.1:5433/course_search")

engine = create_async_engine(DATABASE_URL, echo=False)

import asyncpg
from sqlalchemy import event
from pgvector.asyncpg import register_vector

@event.listens_for(engine.sync_engine, "connect")
def connect(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, asyncpg.Connection):
        pass

# Safe basic init for pgvector + asyncpg

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"

    code = Column(String(50), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    embedding = Column(Vector(EMBEDDING_DIM))

class SavedCourse(Base):
    __tablename__ = "saved_courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(50), index=True, nullable=False)
    course_code = Column(String(50), ForeignKey("courses.code"), nullable=False)
    saved_at = Column(DateTime(timezone=True), server_default=func.now())
