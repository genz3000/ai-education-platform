"""Knowledge Base schemas"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentCreate(BaseModel):
    """Document creation schema"""
    title: str
    type: str = "textbook"
    meta_data: Optional[dict] = None


class DocumentResponse(BaseModel):
    """Document response schema"""
    id: str
    kb_id: str
    title: str
    file_path: Optional[str] = None
    file_type: Optional[str] = None
    status: str
    chunk_count: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    """Search request schema"""
    query: str
    school_id: Optional[str] = None
    limit: int = 10


class SearchResult(BaseModel):
    """Single search result"""
    document_id: str
    chunk_id: str
    content: str
    score: float
    source: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response schema"""
    query: str
    results: List[SearchResult]
    total: int


class KnowledgeTopicResponse(BaseModel):
    """Knowledge graph topic"""
    topic: str
    level: int
    related_topics: List[str]
    question_count: int
    mastery_avg: float