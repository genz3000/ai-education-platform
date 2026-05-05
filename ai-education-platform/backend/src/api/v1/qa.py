"""Q&A API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.database import get_db
from src.schemas.qa import (
    QuestionRequest,
    QuestionResponse,
    ConversationResponse,
    FeedbackRequest
)
from src.services.qa_service import QAService

router = APIRouter()


@router.post("/ask", response_model=QuestionResponse)
async def ask_question(
    request: QuestionRequest,
    db: AsyncSession = Depends(get_db)
):
    """Ask AI question with RAG context"""
    service = QAService(db)
    response = await service.ask(
        question=request.question,
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        mode=request.mode,  # teacher / student / parent
        school_id=request.school_id
    )
    return response


@router.get("/history", response_model=list[ConversationResponse])
async def get_conversation_history(
    user_id: str,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get conversation history"""
    service = QAService(db)
    history = await service.get_history(user_id, limit)
    return history


@router.delete("/history/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete conversation"""
    service = QAService(db)
    await service.delete_conversation(conversation_id)


@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackRequest,
    db: AsyncSession = Depends(get_db)
):
    """Submit feedback for answer quality"""
    service = QAService(db)
    await service.record_feedback(
        message_id=feedback.message_id,
        rating=feedback.rating,
        comment=feedback.comment
    )
    return {"status": "recorded"}