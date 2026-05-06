"""RAG API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Body
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import json

from src.utils.database import get_db
from src.rag.pipeline import create_rag_pipeline, create_rag_query_engine
from src.rag.document_processor import create_document_processor
from src.rag.embeddings import EmbeddingService
from src.schemas.knowledge import DocumentCreate, DocumentResponse
from src.models.knowledge import Document, DocumentChunk, KnowledgeBase
from src.api.v1.auth import get_current_active_user
from src.models.user import User
from src.utils.logger import Logger

logger = Logger(__name__)
router = APIRouter()


# Request schemas
class RAGQueryRequest(BaseModel):
    query: str
    school_id: str
    top_k: int = 5


@router.post("/upload/{kb_id}")
async def upload_document(
    kb_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload and process a document"""
    try:
        # Read file content
        content = await file.read()
        
        # Process document
        processor = create_document_processor()
        processed = await processor.process_file(
            file_content=content,
            filename=file.filename,
            metadata={"uploaded_by": current_user.username}
        )
        
        # Create document record
        doc = Document(
            kb_id=kb_id,
            title=file.filename,
            file_type=processed.file_type,
            content=processed.content,
            file_size=len(content),
            metadata=processed.metadata
        )
        db.add(doc)
        await db.flush()
        
        # Process with RAG pipeline
        pipeline = create_rag_pipeline(db)
        chunk_ids = await pipeline.process_document(
            document_id=str(doc.id),
            content=processed.content,
            metadata=processed.metadata
        )
        
        return {
            "id": str(doc.id),
            "title": doc.title,
            "chunk_count": len(chunk_ids),
            "file_type": processed.file_type,
            "language": processed.language
        }
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query")
async def rag_query(
    request: RAGQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """Query the RAG system"""
    try:
        engine = create_rag_query_engine(db)
        result = await engine.query_with_sources(request.query, request.school_id, request.top_k)
        
        return result
        
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/stream")
async def rag_query_stream(
    request: RAGQueryRequest,
    db: AsyncSession = Depends(get_db)
):
    """Query RAG and stream results"""
    from fastapi.responses import StreamingResponse
    import json
    
    async def generate():
        try:
            engine = create_rag_query_engine(db)
            result = await engine.query_with_sources(request.query, request.school_id, request.top_k)
            
            # Stream chunks
            for i, chunk in enumerate(result["chunks"]):
                yield f"data: {json.dumps({'chunk': i, 'data': chunk})}\n\n"
            
            yield f"data: {json.dumps({'done': True, 'context_length': len(result['context'])})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


@router.get("/search")
async def search_knowledge(
    query: str,
    school_id: str,
    top_k: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Search knowledge base"""
    try:
        pipeline = create_rag_pipeline(db)
        chunks = await pipeline._retrieve_chunks(query, school_id, top_k)
        
        return {
            "query": query,
            "results": chunks,
            "count": len(chunks)
        }
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/documents/{doc_id}/reprocess")
async def reprocess_document(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Re-process a document (e.g., after editing)"""
    try:
        # Get document
        result = await db.execute(
            select(Document).where(Document.id == doc_id)
        )
        doc = result.scalar_one_or_none()
        
        if not doc:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete existing chunks
        pipeline = create_rag_pipeline(db)
        deleted = await pipeline.delete_document_chunks(doc_id)
        
        # Re-process
        chunk_ids = await pipeline.process_document(
            document_id=doc_id,
            content=doc.content,
            metadata=doc.metadata
        )
        
        return {
            "document_id": doc_id,
            "chunks_recreated": len(chunk_ids),
            "chunks_deleted": deleted
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Reprocess error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/{school_id}")
async def get_rag_stats(
    school_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get RAG statistics for a school"""
    from sqlalchemy import func, select
    from src.models.knowledge import Document, KnowledgeBase
    
    try:
        # Count documents
        doc_count = await db.execute(
            select(func.count(Document.id))
            .join(KnowledgeBase, Document.kb_id == KnowledgeBase.id)
            .where(KnowledgeBase.school_id == school_id)
        )
        
        # Count chunks
        chunk_count = await db.execute(
            select(func.count(DocumentChunk.id))
            .join(Document, DocumentChunk.document_id == Document.id)
            .join(KnowledgeBase, Document.kb_id == KnowledgeBase.id)
            .where(KnowledgeBase.school_id == school_id)
        )
        
        return {
            "school_id": school_id,
            "document_count": doc_count.scalar() or 0,
            "chunk_count": chunk_count.scalar() or 0
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch/process")
async def batch_process_documents(
    documents: List[dict],
    school_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Batch process multiple documents"""
    try:
        processor = create_document_processor()
        pipeline = create_rag_pipeline(db)
        
        processed_docs = []
        
        for doc_data in documents:
            # Process file
            content = doc_data.get("content", "")
            if isinstance(content, str):
                content = content.encode("utf-8")
            
            processed = await processor.process_file(
                file_content=content,
                filename=doc_data.get("filename", "unknown.txt"),
                metadata=doc_data.get("metadata", {})
            )
            
            # Create document record
            doc = Document(
                kb_id=doc_data.get("kb_id", ""),
                title=doc_data.get("filename", "Unknown"),
                file_type=processed.file_type,
                content=processed.content,
                file_size=len(content),
                metadata=processed.metadata
            )
            db.add(doc)
            await db.flush()
            
            # Process with RAG
            chunk_ids = await pipeline.process_document(
                document_id=str(doc.id),
                content=processed.content,
                metadata=processed.metadata
            )
            
            processed_docs.append({
                "id": str(doc.id),
                "title": doc.title,
                "chunks": len(chunk_ids)
            })
        
        return {
            "processed": len(processed_docs),
            "documents": processed_docs
        }
        
    except Exception as e:
        logger.error(f"Batch process error: {e}")
        raise HTTPException(status_code=500, detail=str(e))