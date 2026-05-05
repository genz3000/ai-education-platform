"""Q&A Service with RAG"""
import uuid
from typing import Optional, List, Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.analytics import ConversationHistory
from src.rag.retriever import RAGRetriever
from src.agents.qa_agent import QAAgent
from src.utils.logger import Logger

logger = Logger(__name__)


class QAService:
    """Q&A Service with AI and RAG"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.retriever = RAGRetriever(db)
        self.agent = QAAgent()
    
    async def ask(
        self,
        question: str,
        user_id: str,
        conversation_id: Optional[str],
        mode: str,
        school_id: str
    ) -> dict:
        """Answer question using RAG + LLM"""
        # Get or create conversation
        conversation = await self._get_or_create_conversation(
            conversation_id, user_id, mode
        )
        
        # Add user message
        messages = conversation.messages or []
        messages.append({
            "role": "user",
            "content": question,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # RAG: Retrieve context
        context_chunks = await self.retriever.retrieve(
            query=question,
            school_id=school_id,
            top_k=5
        )
        
        # Generate answer with LLM
        answer_data = await self.agent.generate_answer(
            question=question,
            context_chunks=context_chunks,
            mode=mode,
            conversation_history=messages[:-1]
        )
        
        # Add assistant message
        messages.append({
            "role": "assistant",
            "content": answer_data["answer"],
            "sources": answer_data.get("sources", []),
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Update conversation
        conversation.messages = messages
        await self.db.commit()
        
        return {
            "answer": answer_data["answer"],
            "conversation_id": str(conversation.id),
            "sources": answer_data.get("sources", []),
            "mode": mode,
            "timestamp": datetime.utcnow()
        }
    
    async def _get_or_create_conversation(
        self,
        conversation_id: Optional[str],
        user_id: str,
        mode: str
    ) -> ConversationHistory:
        """Get existing or create new conversation"""
        if conversation_id:
            result = await self.db.execute(
                select(ConversationHistory).where(
                    ConversationHistory.id == conversation_id
                )
            )
            conversation = result.scalar_one_or_none()
            if conversation:
                return conversation
        
        conversation = ConversationHistory(
            user_id=user_id,
            mode=mode,
            messages=[]
        )
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation
    
    async def get_history(self, user_id: str, limit: int) -> List[dict]:
        """Get conversation history"""
        result = await self.db.execute(
            select(ConversationHistory)
            .where(ConversationHistory.user_id == user_id)
            .order_by(ConversationHistory.updated_at.desc())
            .limit(limit)
        )
        conversations = result.scalars().all()
        
        return [
            {
                "id": str(c.id),
                "user_id": str(c.user_id),
                "mode": c.mode,
                "messages": c.messages,
                "last_message": c.messages[-1]["content"] if c.messages else None,
                "created_at": c.created_at
            }
            for c in conversations
        ]
    
    async def delete_conversation(self, conversation_id: str):
        """Delete conversation"""
        result = await self.db.execute(
            select(ConversationHistory).where(
                ConversationHistory.id == conversation_id
            )
        )
        conversation = result.scalar_one_or_none()
        if conversation:
            await self.db.delete(conversation)
            await self.db.commit()
    
    async def record_feedback(
        self,
        message_id: str,
        rating: int,
        comment: Optional[str]
    ):
        """Record feedback for answer quality"""
        # TODO: Update conversation rating
        logger.info(f"Recorded feedback: {message_id}, rating: {rating}")