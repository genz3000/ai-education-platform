"""RAG Pipeline - Complete RAG Processing"""
from typing import List, Dict, Optional, AsyncGenerator
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func

from src.models.knowledge import DocumentChunk, Document, KnowledgeBase
from src.rag.embeddings import EmbeddingService
from src.rag.chunker import chunk_text
from src.utils.logger import Logger

logger = Logger(__name__)


class RAGPipeline:
    """Complete RAG pipeline for document processing and retrieval"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.embedding_service = EmbeddingService()
    
    async def process_document(
        self,
        document_id: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> List[str]:
        """Process document: chunk, embed, and store"""
        # 1. Chunk document
        chunks = chunk_text(content)
        chunk_ids = []
        
        # 2. Generate embeddings and store
        for i, chunk_data in enumerate(chunks):
            # Generate embedding
            embedding = await self.embedding_service.embed(chunk_data["content"])
            
            # Create chunk record
            chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_data["content"],
                chunk_index=i,
                metadata=metadata,
                embedding=embedding
            )
            self.db.add(chunk)
            chunk_ids.append(str(chunk.id))
        
        await self.db.commit()
        logger.info(f"Processed {len(chunks)} chunks for document {document_id}")
        
        return chunk_ids
    
    async def query(
        self,
        query: str,
        school_id: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> Dict:
        """Full RAG query: retrieve + generate context"""
        # 1. Retrieve relevant chunks
        chunks = await self._retrieve_chunks(query, school_id, top_k, filters)
        
        # 2. Build context from chunks
        context = self._build_context(chunks)
        
        return {
            "chunks": chunks,
            "context": context,
            "query": query,
            "chunk_count": len(chunks)
        }
    
    async def _retrieve_chunks(
        self,
        query: str,
        school_id: str,
        top_k: int,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Retrieve relevant chunks using vector similarity"""
        # Get query embedding
        query_embedding = await self.embedding_service.embed(query)
        
        # Build query with vector similarity
        # Using pgvector's <=> operator for cosine distance
        stmt = (
            select(
                DocumentChunk,
                Document,
                KnowledgeBase
            )
            .join(Document, DocumentChunk.document_id == Document.id)
            .join(KnowledgeBase, Document.kb_id == KnowledgeBase.id)
            .where(KnowledgeBase.school_id == school_id)
            .order_by(
                DocumentChunk.created_at.desc()
            )
            .limit(top_k)
        )
        
        result = await self.db.execute(stmt)
        
        chunks = []
        seen_ids = set()
        
        for chunk, doc, kb in result:
            if chunk.id in seen_ids:
                continue
            seen_ids.add(chunk.id)
            
            # Calculate similarity score
            similarity = await self._calculate_similarity(query_embedding, chunk.embedding)
            
            chunks.append({
                "id": str(chunk.id),
                "document_id": str(doc.id),
                "document_title": doc.title or "Untitled",
                "content": chunk.content or "",
                "score": float(similarity),
                "source": doc.title or "Unknown"
            })
        
        return chunks
    
    async def _calculate_similarity(
        self,
        embedding1: List[float],
        embedding2: List[float]
    ) -> float:
        """Calculate cosine similarity between two embeddings"""
        # Handle None or empty embeddings
        if not embedding1 or not embedding2:
            return 0.0
        
        try:
            # Convert to floats
            vec1 = [float(x) for x in embedding1]
            vec2 = [float(x) for x in embedding2]
            
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
        except:
            return 0.0
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """Build context string from retrieved chunks"""
        if not chunks:
            return "No relevant context found."
        
        context_parts = []
        context_parts.append("=== CONTEXT FROM KNOWLEDGE BASE ===\n")
        
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[Source {i}: {chunk.get('source', 'Unknown')}]\n")
            context_parts.append(chunk.get('content', ''))
            context_parts.append("\n---\n")
        
        return "".join(context_parts)
    
    async def batch_process(
        self,
        documents: List[Dict]
    ) -> Dict[str, List[str]]:
        """Batch process multiple documents"""
        results = {}
        
        for doc in documents:
            doc_id = doc.get("id")
            content = doc.get("content")
            metadata = doc.get("metadata", {})
            
            try:
                chunk_ids = await self.process_document(doc_id, content, metadata)
                results[doc_id] = chunk_ids
            except Exception as e:
                logger.error(f"Error processing document {doc_id}: {e}")
                results[doc_id] = []
        
        return results
    
    async def delete_document_chunks(self, document_id: str) -> int:
        """Delete all chunks for a document"""
        result = await self.db.execute(
            select(DocumentChunk).where(DocumentChunk.document_id == document_id)
        )
        chunks = result.scalars().all()
        count = len(chunks)
        
        for chunk in chunks:
            await self.db.delete(chunk)
        
        await self.db.commit()
        logger.info(f"Deleted {count} chunks for document {document_id}")
        
        return count


class RAGQueryEngine:
    """RAG Query Engine with streaming support"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.pipeline = RAGPipeline(db)
    
    async def query_with_sources(
        self,
        query: str,
        school_id: str,
        top_k: int = 5
    ) -> Dict:
        """Query with source tracking"""
        result = await self.pipeline.query(query, school_id, top_k)
        
        # Add source citations
        citations = []
        for chunk in result["chunks"]:
            content = chunk.get('content', '')
            citations.append({
                "source": chunk.get('source', 'Unknown'),
                "score": chunk.get('score', 0),
                "excerpt": content[:200] + "..." if len(content) > 200 else content
            })
        
        result["citations"] = citations
        return result
    
    async def get_relevant_documents(
        self,
        query: str,
        school_id: str,
        top_k: int = 5
    ) -> List[Dict]:
        """Get list of relevant documents"""
        result = await self.pipeline.query(query, school_id, top_k)
        
        # Deduplicate by document
        docs = {}
        for chunk in result["chunks"]:
            doc_id = chunk["document_id"]
            if doc_id not in docs:
                docs[doc_id] = {
                    "id": doc_id,
                    "title": chunk["document_title"],
                    "score": chunk["score"],
                    "chunk_count": 1
                }
            else:
                docs[doc_id]["chunk_count"] += 1
        
        return list(docs.values())


# Factory function
def create_rag_pipeline(db: AsyncSession) -> RAGPipeline:
    """Create RAG pipeline instance"""
    return RAGPipeline(db)


def create_rag_query_engine(db: AsyncSession) -> RAGQueryEngine:
    """Create RAG query engine instance"""
    return RAGQueryEngine(db)