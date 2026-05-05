"""User database model"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
import enum

from src.utils.database import Base


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.STUDENT)
    school_id = Column(UUID(as_uuid=True), nullable=True)
    full_name = Column(String(200))
    phone = Column(String(20))
    avatar_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(String(10), default="true")
    
    def set_password(self, password: str):
        """Hash and set password"""
        from src.utils.security import get_password_hash
        self.password_hash = get_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        from src.utils.security import verify_password
        return verify_password(password, self.password_hash)
    
    def __repr__(self):
        return f"<User {self.email}>"