"""Assessment AI Agent for Question Generation and Grading"""
from typing import List, Dict
from src.config import settings
from src.utils.logger import Logger

logger = Logger(__name__)


class AssessmentAgent:
    """Assessment AI Agent"""
    
    def __init__(self):
        self.llm_type = "openai"
    
    async def generate_questions(
        self,
        topic: str,
        difficulty: int,
        count: int,
        types: List[str],
        exam_type: str
    ) -> List[Dict]:
        """Generate assessment questions using AI"""
        # TODO: Use actual LLM call
        # Build prompt for question generation
        
        questions = []
        for i in range(count):
            q_type = types[i % len(types)]
            question = {
                "type": q_type,
                "content": f"示例{topic}題目 {i+1} (難度: {difficulty})",
                "options": [{"A": "選項A"}, {"B": "選項B"}, {"C": "選項C"}, {"D": "選項D"}] if q_type == "mcq" else None,
                "answer": "A" if q_type == "mcq" else "示例答案"
            }
            questions.append(question)
        
        return questions
    
    async def grade_answer(
        self,
        question_content: str,
        correct_answer: str,
        student_answer: str,
        question_type: str
    ) -> Dict:
        """Grade student answer using AI"""
        # TODO: Use actual LLM for semantic grading
        
        if question_type == "mcq":
            is_correct = student_answer.strip().upper() == correct_answer.strip().upper()
            score = "100%" if is_correct else "0%"
        else:
            # For subjective questions, use LLM grading
            # is_correct = await self._llm_grade(question_content, correct_answer, student_answer)
            is_correct = len(student_answer) > 10  # Placeholder
            score = "85%" if is_correct else "70%"
        
        return {
            "is_correct": is_correct,
            "score": score,
            "feedback": f"你的答案{'正確' if is_correct else '需要改進'}。",
            "explanation": "詳細解釋將由 AI 生成。"
        }
    
    async def generate_feedback(
        self,
        assessment_id: str,
        topic: str,
        score: int
    ) -> Dict:
        """Generate comprehensive feedback for assessment"""
        strong_topics = []
        weak_topics = []
        recommendations = []
        
        if score >= 80:
            strong_topics.append(topic)
            recommendations.append("繼續保持當前學習節奏，挑戰更高難度題目")
        elif score >= 60:
            recommendations.append(f"複習 {topic} 的基礎概念，多做練習")
        else:
            weak_topics.append(topic)
            recommendations.append(f"建議重新學習 {topic} 相關章節，從基礎題開始")
        
        return {
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "recommendations": recommendations
        }