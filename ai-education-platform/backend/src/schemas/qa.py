"""Q&A schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class QuestionRequest(BaseModel):
    """Question request schema"""
    question: str
    user_id: str
    conversation_id: Optional[str] = None
    mode: str = "student"  # teacher, student, parent
    school_id: Optional[str] = None
    context: Optional[Dict] = None  # Additional context


class AnswerSource(BaseModel):
    """Source for the answer"""
    document_id: str
    chunk_id: str
    content: str
    page: Optional[int] = None
    score: float


class QuestionResponse(BaseModel):
    """Question response schema"""
    answer: str
    conversation_id: str
    sources: List[AnswerSource]
    mode: str
    timestamp: datetime


class ConversationMessage(BaseModel):
    """Single message in conversation"""
    role: str  # user, assistant
    content: str
    timestamp: datetime


class ConversationResponse(BaseModel):
    """Conversation history item"""
    id: str
    user_id: str
    mode: str
    messages: List[ConversationMessage]
    last_message: Optional[str] = None
    created_at: datetime


class FeedbackRequest(BaseModel):
    """Feedback submission schema"""
    message_id: str
    rating: int  # 1-5
    comment: Optional[str] = None