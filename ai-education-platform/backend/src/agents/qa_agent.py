"""Q&A AI Agent"""
from typing import List, Dict, Optional
from src.config import settings
from src.utils.logger import Logger

logger = Logger(__name__)


class QAAgent:
    """Q&A AI Agent using LLM"""
    
    def __init__(self):
        self.llm_type = "openai"  # or "anthropic"
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict],
        mode: str,
        conversation_history: List[Dict]
    ) -> Dict:
        """Generate answer using LLM with RAG context"""
        # Build context from chunks
        context = self._build_context(context_chunks)
        
        # Build system prompt based on mode
        system_prompt = self._get_system_prompt(mode)
        
        # Build conversation history
        history_context = self._format_history(conversation_history)
        
        # Generate answer
        # TODO: Use actual LLM call
        # from openai import OpenAI
        # client = OpenAI(api_key=settings.OPENAI_API_KEY)
        # response = client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": f"Context:\n{context}\n\nHistory:\n{history_context}\n\nQuestion: {question}"}
        #     ]
        # )
        # answer = response.choices[0].message.content
        
        # Placeholder response
        answer = f"根據提供的教材內容，我來回答你的問題：{question}\n\n[答案將由 LLM 生成]"
        
        return {
            "answer": answer,
            "sources": [
                {
                    "document_id": c["document_id"],
                    "content": c["content"][:200],
                    "score": c["score"]
                }
                for c in context_chunks[:3]
            ]
        }
    
    def _build_context(self, chunks: List[Dict]) -> str:
        """Build context string from chunks"""
        if not chunks:
            return "沒有找到相關內容。"
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(f"[來源 {i}]\n{chunk['content']}\n")
        
        return "\n".join(context_parts)
    
    def _get_system_prompt(self, mode: str) -> str:
        """Get system prompt based on mode"""
        prompts = {
            "teacher": "你是一位經驗豐富的教師，擅長解釋概念、生成教案和提供教學建議。回答要專業、詳細、有幫助。",
            "student": "你是一位耐心的導師，擅長用簡單易懂的語言解釋概念，引導學生思考。回答要鼓勵性、清晰、有啟發性。",
            "parent": "你是一位教育顧問，幫助家長了解子女的學習情況。回答要友善、實際、有建設性。"
        }
        return prompts.get(mode, prompts["student"])
    
    def _format_history(self, history: List[Dict]) -> str:
        """Format conversation history"""
        if not history:
            return ""
        
        parts = []
        for msg in history[-5:]:  # Last 5 messages
            role = "用戶" if msg["role"] == "user" else "助手"
            parts.append(f"{role}: {msg['content'][:100]}...")
        
        return "\n".join(parts)