"""Seed database with sample data"""
import asyncio
from datetime import datetime

from src.utils.database import AsyncSessionLocal
from src.models.user import User, UserRole
from src.models.knowledge import KnowledgeBase, Document
from src.models.question import Question


async def seed_data():
    """Seed database with sample data"""
    async with AsyncSessionLocal() as db:
        # Create sample users
        admin = User(
            email="admin@school.edu.hk",
            username="admin",
            role=UserRole.ADMIN,
            school_id=None
        )
        admin.set_password("admin123")
        
        teacher = User(
            email="teacher@school.edu.hk",
            username="teacher",
            role=UserRole.TEACHER,
            school_id=None
        )
        teacher.set_password("teacher123")
        
        student = User(
            email="student@school.edu.hk",
            username="student",
            role=UserRole.STUDENT,
            school_id=None
        )
        student.set_password("student123")
        
        db.add_all([admin, teacher, student])
        await db.commit()
        
        print("Sample data seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())