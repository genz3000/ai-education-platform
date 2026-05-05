"""Learning Analytics models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Float, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from src.utils.database import Base


class LearningRecord(Base):
    """Student learning behavior records"""
    __tablename__ = "learning_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_type = Column(String(50), nullable=False)  # query, answer, read, etc.
    event_data = Column(JSONB)  # Detailed event info
    topic = Column(String(200))
    duration = Column(Integer)  # seconds
    result = Column(String(50))  # correct/incorrect
    meta_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)


class TopicMastery(Base):
    """Student mastery level per topic"""
    __tablename__ = "topic_mastery"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    topic = Column(String(200), nullable=False)
    curriculum_code = Column(String(100))
    mastery_level = Column(Float, default=0.0)  # 0.0 - 1.0
    questions_attempted = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    accuracy = Column(Float, default=0.0)
    last_practiced = Column(DateTime)
    risk_level = Column(String(20))  # high, medium, low
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConversationHistory(Base):
    """Q&A conversation history"""
    __tablename__ = "conversation_history"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    mode = Column(String(50))  # teacher, student, parent
    messages = Column(JSONB)  # [{"role": "user", "content": "..."}]
    rating = Column(Integer)  # 1-5
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)