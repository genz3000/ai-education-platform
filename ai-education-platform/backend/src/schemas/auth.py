"""Authentication schemas"""
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
from uuid import UUID


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
    
    @field_validator('id', mode='before')
    @classmethod
    def convert_id(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v
    
    class Config:
        from_attributes = True


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: str
    user_id: str
    role: str
    exp: datetime