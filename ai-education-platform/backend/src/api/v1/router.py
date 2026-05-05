"""API v1 Router"""
from fastapi import APIRouter

from src.api.v1 import auth, knowledge, qa, assessment, analytics

api_router = APIRouter()

# Include all module routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["Knowledge Base"])
api_router.include_router(qa.router, prefix="/qa", tags=["Q&A"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])