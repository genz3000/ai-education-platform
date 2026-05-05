"""Knowledge Base API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.utils.database import get_db
from src.schemas.knowledge import (
    DocumentResponse,
    DocumentCreate,
    SearchRequest,
    SearchResponse,
    KnowledgeTopicResponse
)
from src.services.knowledge_service import KnowledgeService

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = "",
    kb_type: str = "textbook",
    school_id: str = "",
    db: AsyncSession = Depends(get_db)
):
    """Upload and process document"""
    service = KnowledgeService(db)
    result = await service.process_upload(file, title, kb_type, school_id)
    return result


@router.get("/search", response_model=SearchResponse)
async def search_knowledge(
    query: str,
    school_id: str = "",
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """Search knowledge base"""
    service = KnowledgeService(db)
    results = await service.search(query, school_id, limit)
    return {"query": query, "results": results, "total": len(results)}


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get document by ID"""
    service = KnowledgeService(db)
    document = await service.get_document(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete document"""
    service = KnowledgeService(db)
    await service.delete_document(document_id)


@router.get("/topics/knowledge-graph", response_model=List[KnowledgeTopicResponse])
async def get_knowledge_graph(
    school_id: str = "",
    db: AsyncSession = Depends(get_db)
):
    """Get knowledge graph/topics"""
    service = KnowledgeService(db)
    topics = await service.get_topics(school_id)
    return topics