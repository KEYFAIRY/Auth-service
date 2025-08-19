from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.shared.enums import PianoLevel


class CreateUserRequest(BaseModel):
    """Esquema para la petición de crear usuario"""
    uid: str = Field(..., min_length=1, description="Firebase UID del usuario")
    email: str = Field(..., min_length=5, max_length=255, description="Email del usuario")
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    piano_level: PianoLevel = Field(..., description="Nivel de piano del usuario")
    
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
                "piano_level": "beginner"
            }
        }


class UserResponse(BaseModel):
    """Esquema para la respuesta de usuario"""
    uid: str
    email: str
    name: str
    piano_level: str
    
    class Config:
        from_attributes = True
        schema_extra = {
            "example": {
                "uid": "firebase_uid_123",
                "email": "usuario@example.com",
                "name": "Juan Pérez",
                "piano_level": "beginner"
            }
        }


class UpdateUserRequest(BaseModel):
    """Esquema para actualizar usuario"""
    email: Optional[str] = Field(None, min_length=5, max_length=255, description="Nuevo email del usuario")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nuevo nombre del usuario")
    piano_level: Optional[PianoLevel] = Field(None, description="Nuevo nivel de piano")
    
    @validator('email')
    def validate_email(cls, v):
        if v:
            v = v.strip().lower()
            if '@' not in v or '.' not in v.split('@')[1]:
                raise ValueError('Invalid email format')
        return v
    
    @validator('name')
    def validate_name(cls, v):
        if v:
            v = v.strip()
            if not v:
                raise ValueError('Name cannot be empty')
        return v

    class Config:
        schema_extra = {
            "example": {
                "email": "nuevo_email@example.com",
                "name": "Juan Carlos Pérez",
                "piano_level": "intermediate"
            }
        }