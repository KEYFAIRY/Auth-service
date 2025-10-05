from typing import Optional
from pydantic import BaseModel, Field, validator
from app.shared.enums import PianoLevel


class CreateUserRequest(BaseModel):
    """Schema for creating a user"""
    uid: str = Field(..., min_length=1, description="Firebase UID")
    email: str = Field(..., min_length=5, max_length=255, description="Email ")
    name: str = Field(..., min_length=2, max_length=100, description="Full name ")
    piano_level: PianoLevel = Field(..., description="Piano level ")

    @validator('email')
    def validate_email(cls, v):
        v = v.strip().lower()
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('Name cannot be empty')
        return v
    
    @validator('uid')
    def validate_uid(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('UID cannot be empty')
        return v

    class Config:
        schema_extra = {
            "example": {
                "uid": "firebase_uid_123",
                "email": "usuario@example.com",
                "name": "Juan Pérez",
                "piano_level": "teclado II"
            }
        }

class UserResponse(BaseModel):
    """Schema for user response"""
    uid: str
    email: str
    name: str
    piano_level: str

    class Config:
        schema_extra = {
            "example": {
                "uid": "firebase_uid_123",
                "email": "usuario@example.com",
                "name": "Juan Pérez",
                "piano_level": "beginner"
            }
        }
        
class UpdateUserRequest(BaseModel):
    """Schema for updating a user"""
    piano_level: Optional[PianoLevel] = Field(None, description="New piano level")