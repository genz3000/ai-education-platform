"""Empty init file for schemas module"""
from src.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from src.schemas.knowledge import DocumentCreate, DocumentResponse, SearchRequest, SearchResponse
from src.schemas.qa import QuestionRequest, QuestionResponse, ConversationResponse
from src.schemas.assessment import GenerateRequest, GenerateResponse, SubmitRequest, SubmitResponse
from src.schemas.analytics import StudentAnalyticsResponse, ClassAnalyticsResponse

__all__ = [
    "UserCreate", "UserLogin", "Token", "UserResponse",
    "DocumentCreate", "DocumentResponse", "SearchRequest", "SearchResponse",
    "QuestionRequest", "QuestionResponse", "ConversationResponse",
    "GenerateRequest", "GenerateResponse", "SubmitRequest", "SubmitResponse",
    "StudentAnalyticsResponse", "ClassAnalyticsResponse"
]