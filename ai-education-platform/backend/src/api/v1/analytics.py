"""Analytics API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import get_db
from src.schemas.analytics import (
    StudentAnalyticsResponse,
    ClassAnalyticsResponse,
    TrendsResponse,
    RecommendationsResponse
)
from src.services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/student/{student_id}", response_model=StudentAnalyticsResponse)
async def get_student_analytics(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get student learning analytics"""
    service = AnalyticsService(db)
    analytics = await service.get_student_analytics(student_id)
    return analytics


@router.get("/class/{class_id}", response_model=ClassAnalyticsResponse)
async def get_class_analytics(
    class_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get class-level analytics"""
    service = AnalyticsService(db)
    analytics = await service.get_class_analytics(class_id)
    return analytics


@router.get("/trends", response_model=TrendsResponse)
async def get_learning_trends(
    school_id: str = "",
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Get learning trends"""
    service = AnalyticsService(db)
    trends = await service.get_trends(school_id, days)
    return trends


@router.get("/recommendations/{student_id}", response_model=RecommendationsResponse)
async def get_recommendations(
    student_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get personalized learning recommendations"""
    service = AnalyticsService(db)
    recommendations = await service.get_recommendations(student_id)
    return recommendations