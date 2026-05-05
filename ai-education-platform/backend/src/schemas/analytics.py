"""Analytics schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class TopicMastery(BaseModel):
    """Topic mastery info"""
    topic: str
    mastery: float  # 0.0 - 1.0
    questions_attempted: int
    accuracy: float
    risk_level: str  # high, medium, low


class LearningTrend(BaseModel):
    """Learning trend data point"""
    date: str
    score: float
    questions_attempted: int
    accuracy: float


class StrongTopic(BaseModel):
    """Strong topic info"""
    topic: str
    mastery: float
    trend: str  # improving, stable, declining


class WeakTopic(BaseModel):
    """Weak topic info"""
    topic: str
    mastery: float
    recommended_practice: int  # suggested questions


class StudentAnalyticsResponse(BaseModel):
    """Student analytics response"""
    student_id: str
    overall_mastery: float
    topic_mastery: List[TopicMastery]
    learning_trends: List[LearningTrend]
    strong_topics: List[StrongTopic]
    weak_topics: List[WeakTopic]
    risk_students: Optional[List[str]] = None
    updated_at: datetime


class ClassStats(BaseModel):
    """Class statistics"""
    topic: str
    avg_mastery: float
    student_count: int
    at_risk_count: int


class ClassAnalyticsResponse(BaseModel):
    """Class analytics response"""
    class_id: str
    student_count: int
    avg_score: float
    topic_stats: List[ClassStats]
    risk_students: List[str]
    recommendations: List[str]
    updated_at: datetime


class TrendDataPoint(BaseModel):
    """Trend data point"""
    date: str
    value: float
    category: Optional[str] = None


class TrendsResponse(BaseModel):
    """Learning trends response"""
    school_id: str
    periods: List[TrendDataPoint]
    topics: List[TrendDataPoint]
    generated_at: datetime


class RecommendationItem(BaseModel):
    """Learning recommendation item"""
    type: str  # practice, review, resource
    topic: str
    content: str
    priority: str  # high, medium, low
    estimated_time: Optional[int] = None  # minutes


class RecommendationsResponse(BaseModel):
    """Learning recommendations response"""
    student_id: str
    recommendations: List[RecommendationItem]
    generated_at: datetime