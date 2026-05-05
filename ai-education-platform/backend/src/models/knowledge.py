"""Knowledge Base database model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from src.utils.database import Base


class KnowledgeBase(Base):
    """Knowledge Base model"""
    __tablename__ = "knowledge_bases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    school_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(50), default="textbook")  # textbook, notes, exam
    curriculum_mapping = Column(JSONB)  # DSE/TSA mapping
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Document(Base):
    """Document model"""
    __tablename__ = "documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kb_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id"), nullable=False)
    title = Column(String(500), nullable=False)
    file_path = Column(String(1000))  # S3 path
    file_type = Column(String(50))  # pdf, docx, pptx, etc.
    file_size = Column(String(50))
    chunk_count = Column(String(20))
    metadata = Column(JSONB)  # title, section, difficulty
    status = Column(String(50), default="processing")  # processing, ready, error
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DocumentChunk(Base):
    """Document chunk with vector embedding"""
    __tablename__ = "document_chunks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    content = Column(Text, nullable=False)
    chunk_index = Column(String(20))  # e.g., "2-1" means chapter 2, chunk 1
    embedding = Column(ARRAY(String))  # Store as text for pgvector
    metadata = Column(JSONB)  # position, page, section
    created_at = Column(DateTime, default=datetime.utcnow)