"""Embedding Service for RAG"""
from typing import List
from src.config import settings
from src.utils.logger import Logger

logger = Logger(__name__)


class EmbeddingService:
    """Text embedding service"""
    
    def __init__(self):
        self.model = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION
        self._client = None
    
    @property
    def client(self):
        """Lazy load OpenAI client"""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=settings.OPENAI_API_KEY)
            except ImportError:
                logger.warning("OpenAI not available, using random embeddings")
                self._client = None
        return self._client
    
    async def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        if self.client:
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=text[:2000]  # Truncate long text
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"OpenAI embedding error: {e}")
        
        # Fallback: simple hash-based embedding (deterministic)
        import hashlib
        hash_bytes = hashlib.sha256(text.encode()).digest()
        return [b / 255.0 for b in hash_bytes[:self.dimension]]
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        return [await self.embed(t) for t in texts]
    
    async def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)