"""Assessment schemas"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class GenerateRequest(BaseModel):
    """Question generation request"""
    topic: str
    difficulty: int = 3  # 1-5
    question_count: int = 10
    question_types: List[str] = ["mcq"]  # mcq, short, essay
    exam_type: str = "school"  # DSE, TSA, school
    student_id: Optional[str] = None


class GeneratedQuestion(BaseModel):
    """Single generated question"""
    id: str
    type: str
    content: str
    options: Optional[List[Dict]] = None
    difficulty: int
    dse_topic: Optional[str] = None
    tsa_topic: Optional[str] = None


class GenerateResponse(BaseModel):
    """Question generation response"""
    assessment_id: str
    questions: List[GeneratedQuestion]
    topic: str
    difficulty: int
    generated_at: datetime


class AnswerItem(BaseModel):
    """Single answer item"""
    question_id: str
    answer: str


class SubmitRequest(BaseModel):
    """Answer submission request"""
    assessment_id: str
    answers: List[AnswerItem]
    student_id: str


class AnswerResult(BaseModel):
    """Single answer result"""
    question_id: str
    is_correct: Optional[bool] = None
    score: Optional[str] = None
    feedback: Optional[str] = None


class SubmitResponse(BaseModel):
    """Answer submission response"""
    assessment_id: str
    results: List[AnswerResult]
    total_score: str
    percentage: int
    graded_at: datetime


class GradingDetail(BaseModel):
    """Detailed grading information"""
    content_score: Optional[int] = None
    organization_score: Optional[int] = None
    language_score: Optional[int] = None
    overall_comment: Optional[str] = None


class GradeResponse(BaseModel):
    """Grading response schema"""
    assessment_id: str
    score: str
    percentage: int
    grading: GradingDetail
    feedback: str
    suggestions: List[str]


class ReportResponse(BaseModel):
    """Assessment report schema"""
    assessment_id: str
    student_id: str
    topic: str
    score: str
    percentage: int
    strong_topics: List[str]
    weak_topics: List[str]
    recommendations: List[str]
    generated_at: datetime