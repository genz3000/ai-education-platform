"""Assessment Service for AI Question Generation and Grading"""
import uuid
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.question import Question, Assessment, StudentAnswer
from src.agents.assessment_agent import AssessmentAgent
from src.utils.logger import Logger

logger = Logger(__name__)


class AssessmentService:
    """Assessment generation and grading service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent = AssessmentAgent()
    
    async def generate(
        self,
        topic: str,
        difficulty: int,
        question_count: int,
        question_types: List[str],
        exam_type: str,
        student_id: Optional[str]
    ) -> dict:
        """Generate assessment questions using AI"""
        # Generate questions
        questions_data = await self.agent.generate_questions(
            topic=topic,
            difficulty=difficulty,
            count=question_count,
            types=question_types,
            exam_type=exam_type
        )
        
        # Store questions
        question_ids = []
        for q_data in questions_data:
            question = Question(
                type=q_data["type"],
                content=q_data["content"],
                options=q_data.get("options"),
                answer=q_data.get("answer"),
                difficulty=difficulty,
                dse_topic=topic if exam_type == "DSE" else None,
                tsa_topic=topic if exam_type == "TSA" else None
            )
            self.db.add(question)
            await self.db.commit()
            await self.db.refresh(question)
            question_ids.append(question.id)
        
        # Create assessment record
        assessment = Assessment(
            student_id=student_id,
            topic=topic,
            difficulty=difficulty,
            exam_type=exam_type,
            question_ids=question_ids,
            status="pending"
        )
        self.db.add(assessment)
        await self.db.commit()
        await self.db.refresh(assessment)
        
        return {
            "assessment_id": str(assessment.id),
            "questions": [
                {
                    "id": str(qid),
                    "type": q_data["type"],
                    "content": q_data["content"],
                    "options": q_data.get("options"),
                    "difficulty": difficulty
                }
                for qid, q_data in zip(question_ids, questions_data)
            ],
            "topic": topic,
            "difficulty": difficulty,
            "generated_at": datetime.utcnow()
        }
    
    async def submit(
        self,
        assessment_id: str,
        answers: List[Dict],
        student_id: str
    ) -> dict:
        """Submit answers and get AI grading"""
        # Get assessment
        result = await self.db.execute(
            select(Assessment).where(Assessment.id == assessment_id)
        )
        assessment = result.scalar_one_or_none()
        
        if not assessment:
            raise ValueError("Assessment not found")
        
        # Get questions
        from sqlalchemy import select
        result = await self.db.execute(
            select(Question).where(Question.id.in_(assessment.question_ids))
        )
        questions = {str(q.id): q for q in result.scalars().all()}
        
        # Grade each answer
        results = []
        for answer_item in answers:
            question_id = answer_item["question_id"]
            answer_text = answer_item["answer"]
            
            question = questions.get(question_id)
            if not question:
                continue
            
            # AI grading
            grading = await self.agent.grade_answer(
                question_content=question.content,
                correct_answer=question.answer,
                student_answer=answer_text,
                question_type=question.type
            )
            
            # Store answer
            student_answer = StudentAnswer(
                assessment_id=assessment_id,
                question_id=question_id,
                student_id=student_id,
                answer=answer_text,
                is_correct=grading.get("is_correct"),
                score=grading.get("score"),
                feedback=grading.get("feedback")
            )
            self.db.add(student_answer)
            
            results.append({
                "question_id": question_id,
                "is_correct": grading.get("is_correct"),
                "score": grading.get("score"),
                "feedback": grading.get("feedback")
            })
        
        # Update assessment
        correct_count = sum(1 for r in results if r.get("is_correct"))
        total = len(results)
        percentage = int(correct_count / total * 100) if total > 0 else 0
        
        assessment.score = f"{correct_count}/{total}"
        assessment.percentage = percentage
        assessment.status = "graded"
        assessment.submitted_at = datetime.utcnow()
        assessment.graded_at = datetime.utcnow()
        
        await self.db.commit()
        
        return {
            "assessment_id": assessment_id,
            "results": results,
            "total_score": f"{correct_count}/{total}",
            "percentage": percentage,
            "graded_at": datetime.utcnow()
        }
    
    async def get_report(self, assessment_id: str) -> Optional[dict]:
        """Get detailed assessment report"""
        result = await self.db.execute(
            select(Assessment).where(Assessment.id == assessment_id)
        )
        assessment = result.scalar_one_or_none()
        
        if not assessment:
            return None
        
        # Get feedback
        feedback = await self.agent.generate_feedback(
            assessment_id=assessment_id,
            topic=assessment.topic,
            score=assessment.percentage
        )
        
        return {
            "assessment_id": assessment_id,
            "student_id": str(assessment.student_id),
            "topic": assessment.topic,
            "score": assessment.score,
            "percentage": assessment.percentage,
            "strong_topics": feedback.get("strong_topics", []),
            "weak_topics": feedback.get("weak_topics", []),
            "recommendations": feedback.get("recommendations", []),
            "generated_at": assessment.graded_at or datetime.utcnow()
        }