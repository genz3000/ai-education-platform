"""Question and Assessment models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from src.utils.database import Base


class Question(Base):
    """Question model"""
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kb_id = Column(UUID(as_uuid=True), ForeignKey("knowledge_bases.id"))
    type = Column(String(50), nullable=False)  # mcq, short, essay
    content = Column(Text, nullable=False)  # Question text
    options = Column(JSONB)  # For MCQ: [{"A": "..."}, {"B": "..."}]
    answer = Column(Text)  # Correct answer(s)
    explanation = Column(Text)  # Answer explanation
    difficulty = Column(Integer, default=3)  # 1-5
    dse_topic = Column(String(200))  # DSE topic mapping
    tsa_topic = Column(String(200))  # TSA topic mapping
    curriculum_code = Column(String(100))
    meta_data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Assessment(Base):
    """Assessment/Test model"""
    __tablename__ = "assessments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    topic = Column(String(200), nullable=False)
    difficulty = Column(Integer, default=3)
    exam_type = Column(String(50))  # DSE, TSA, school
    question_ids = Column(ARRAY(UUID))
    score = Column(String(20))  # e.g., "85/100"
    percentage = Column(Integer)
    status = Column(String(50), default="pending")  # pending, submitted, graded
    feedback = Column(Text)
    meta_data = Column(JSONB)
    generated_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime)
    graded_at = Column(DateTime)


class StudentAnswer(Base):
    """Student answer records"""
    __tablename__ = "student_answers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.id"), nullable=False)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean)
    auto_grade = Column(JSONB)  # AI grading result
    score = Column(String(20))
    feedback = Column(Text)
    time_spent = Column(Integer)  # seconds
    created_at = Column(DateTime, default=datetime.utcnow)