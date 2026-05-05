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
    
    async def embed(self, text: str) -> List[float]:
        """Generate embedding for text"""
        # TODO: Implement with OpenAI or local model
        # Using OpenAI:
        # from openai import OpenAI
        # client = OpenAI()
        # response = client.embeddings.create(
        #     model=self.model,
        #     input=text
        # )
        # return response.data[0].embedding
        
        # Placeholder: return random vector
        import random
        return [random.random() for _ in range(self.dimension)]
    
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        # TODO: Implement batch embedding
        return [await self.embed(t) for t in texts]
    
    async def similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0
        
        return dot_product / (magnitude1 * magnitude2)