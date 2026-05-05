"""Authentication schemas"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"


class UserCreate(BaseModel):
    """User creation schema"""
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.STUDENT
    school_id: Optional[str] = None


class UserLogin(BaseModel):
    """User login schema"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    username: str
    role: str
    school_id: Optional[str] = None
    full_name: Optional[str] = None
    is_active: str = "true"
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str
    user_id: str
    role: str
    exp: datetime