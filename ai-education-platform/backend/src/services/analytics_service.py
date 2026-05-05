"""Analytics Service for Learning Insights"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.models.analytics import LearningRecord, TopicMastery
from src.models.question import Assessment
from src.utils.logger import Logger

logger = Logger(__name__)


class AnalyticsService:
    """Learning analytics service"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_student_analytics(self, student_id: str) -> dict:
        """Get comprehensive student analytics"""
        # Get topic mastery
        result = await self.db.execute(
            select(TopicMastery).where(TopicMastery.student_id == student_id)
        )
        mastery_records = result.scalars().all()
        
        topic_mastery = [
            {
                "topic": m.topic,
                "mastery": m.mastery_level,
                "questions_attempted": m.questions_attempted,
                "accuracy": m.accuracy,
                "risk_level": m.risk_level or "medium"
            }
            for m in mastery_records
        ]
        
        # Calculate overall mastery
        overall_mastery = sum(m.mastery_level for m in mastery_records) / len(mastery_records) if mastery_records else 0
        
        # Get learning trends
        trends = await self._get_learning_trends(student_id, days=30)
        
        # Identify strong/weak topics
        sorted_mastery = sorted(topic_mastery, key=lambda x: x["mastery"], reverse=True)
        strong_topics = [
            {"topic": t["topic"], "mastery": t["mastery"], "trend": "stable"}
            for t in sorted_mastery[:5] if t["mastery"] > 0.7
        ]
        weak_topics = [
            {
                "topic": t["topic"],
                "mastery": t["mastery"],
                "recommended_practice": max(10, int((1 - t["mastery"]) * 50))
            }
            for t in sorted_mastery[-5:] if t["mastery"] < 0.5
        ]
        
        return {
            "student_id": student_id,
            "overall_mastery": round(overall_mastery, 2),
            "topic_mastery": topic_mastery,
            "learning_trends": trends,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "updated_at": datetime.utcnow()
        }
    
    async def _get_learning_trends(self, student_id: str, days: int) -> List[dict]:
        """Get learning trends over time"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        result = await self.db.execute(
            select(
                func.date(LearningRecord.created_at).label("date"),
                func.count(LearningRecord.id).label("count"),
                func.avg(
                    func.case(
                        (LearningRecord.result == "correct", 1),
                        else_=0
                    )
                ).label("accuracy")
            )
            .where(
                LearningRecord.student_id == student_id,
                LearningRecord.created_at >= start_date
            )
            .group_by(func.date(LearningRecord.created_at))
            .order_by(func.date(LearningRecord.created_at))
        )
        
        trends = []
        for row in result:
            trends.append({
                "date": str(row.date),
                "questions_attempted": row.count,
                "accuracy": round(row.accuracy or 0, 2) if row.accuracy else 0
            })
        
        return trends
    
    async def get_class_analytics(self, class_id: str) -> dict:
        """Get class-level analytics"""
        # TODO: Implement class-level aggregation
        # 1. Get all students in class
        # 2. Aggregate their analytics
        # 3. Calculate class statistics
        
        return {
            "class_id": class_id,
            "student_count": 0,
            "avg_score": 0.0,
            "topic_stats": [],
            "risk_students": [],
            "recommendations": [],
            "updated_at": datetime.utcnow()
        }
    
    async def get_trends(self, school_id: str, days: int) -> dict:
        """Get school-wide learning trends"""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # TODO: Aggregate school-wide trends
        
        return {
            "school_id": school_id,
            "periods": [],
            "topics": [],
            "generated_at": datetime.utcnow()
        }
    
    async def get_recommendations(self, student_id: str) -> dict:
        """Get personalized learning recommendations"""
        # Get student analytics
        analytics = await self.get_student_analytics(student_id)
        
        recommendations = []
        
        # Generate recommendations based on weak topics
        for weak in analytics.get("weak_topics", []):
            recommendations.append({
                "type": "practice",
                "topic": weak["topic"],
                "content": f"建議練習 {weak['recommended_practice']} 題 {weak['topic']} 相關題目",
                "priority": "high" if weak["mastery"] < 0.3 else "medium",
                "estimated_time": weak["recommended_practice"] * 3  # 3 min per question
            })
        
        return {
            "student_id": student_id,
            "recommendations": recommendations,
            "generated_at": datetime.utcnow()
        }