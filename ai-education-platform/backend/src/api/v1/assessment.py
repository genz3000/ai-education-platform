"""Assessment API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import get_db
from src.schemas.assessment import (
    GenerateRequest,
    GenerateResponse,
    SubmitRequest,
    SubmitResponse,
    GradeResponse,
    ReportResponse
)
from src.services.assessment_service import AssessmentService

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
async def generate_assessment(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """Generate AI assessment questions"""
    service = AssessmentService(db)
    result = await service.generate(
        topic=request.topic,
        difficulty=request.difficulty,
        question_count=request.question_count,
        question_types=request.question_types,
        exam_type=request.exam_type,  # DSE / TSA / school
        student_id=request.student_id
    )
    return result


@router.post("/submit", response_model=SubmitResponse)
async def submit_answers(
    request: SubmitRequest,
    db: AsyncSession = Depends(get_db)
):
    """Submit answers for grading"""
    service = AssessmentService(db)
    result = await service.submit(
        assessment_id=request.assessment_id,
        answers=request.answers,
        student_id=request.student_id
    )
    return result


@router.get("/{assessment_id}/report", response_model=ReportResponse)
async def get_assessment_report(
    assessment_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed assessment report"""
    service = AssessmentService(db)
    report = await service.get_report(assessment_id)
    
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    return report