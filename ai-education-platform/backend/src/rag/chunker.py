"""Document chunking utilities"""
from typing import List, Dict
import re


class ChunkConfig:
    """Configuration for document chunking"""
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        min_chunk_size: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.min_chunk_size = min_chunk_size


def chunk_text(text: str, config: ChunkConfig = None) -> List[Dict]:
    """Split text into chunks with overlap"""
    if config is None:
        config = ChunkConfig()
    
    # Clean text
    text = clean_text(text)
    
    chunks = []
    
    # Split by paragraphs first
    paragraphs = text.split("\n\n")
    
    current_chunk = ""
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # If single paragraph is too large, split it further
        if para_size > config.chunk_size:
            # Add current chunk if not empty
            if current_chunk:
                chunks.append({
                    "content": current_chunk.strip(),
                    "size": current_size
                })
            
            # Split large paragraph
            sub_chunks = split_by_sentences(para, config.chunk_size, config.chunk_overlap)
            chunks.extend(sub_chunks)
            
            current_chunk = ""
            current_size = 0
            continue
        
        # Check if adding this paragraph exceeds chunk size
        if current_size + para_size > config.chunk_size and current_chunk:
            # Save current chunk
            chunks.append({
                "content": current_chunk.strip(),
                "size": current_size
            })
            
            # Start new chunk with overlap
            overlap_text = current_chunk[-config.chunk_overlap:] if current_size > config.chunk_overlap else ""
            current_chunk = overlap_text + para
            current_size = len(current_chunk)
        else:
            # Add to current chunk
            if current_chunk:
                current_chunk += "\n\n" + para
            else:
                current_chunk = para
            current_size += para_size
    
    # Add last chunk
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "size": len(current_chunk)
        })
    
    # Filter small chunks
    chunks = [c for c in chunks if c["size"] >= config.min_chunk_size]
    
    # Add metadata
    for i, chunk in enumerate(chunks):
        chunk["index"] = i
        chunk["total"] = len(chunks)
    
    return chunks


def split_by_sentences(text: str, max_size: int, overlap: int) -> List[Dict]:
    """Split text by sentences while respecting max size"""
    # Split into sentences
    sentences = re.split(r'[。.!？?]+', text)
    
    chunks = []
    current_chunk = ""
    current_size = 0
    
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        
        sent_size = len(sent)
        
        if current_size + sent_size > max_size and current_chunk:
            chunks.append({
                "content": current_chunk.strip(),
                "size": current_size
            })
            
            # Start new chunk with overlap
            overlap_text = current_chunk[-overlap:] if current_size > overlap else ""
            current_chunk = overlap_text + sent
            current_size = len(current_chunk)
        else:
            current_chunk += ("。" if current_chunk else "") + sent
            current_size += sent_size
    
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "size": len(current_chunk)
        })
    
    return chunks


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep Chinese and basic punctuation
    text = re.sub(r'[^\w\s\u4e00-\u9fff，。！？、：；""''（）【】《》]', '', text)
    
    return text.strip()