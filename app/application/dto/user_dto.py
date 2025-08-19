from pydantic import BaseModel, Field, validator
from typing import Optional
from app.shared.enums import PianoLevel


class CreateUserDTO(BaseModel):
    """DTO para crear usuario"""
    uid: str = Field(..., min_length=1, description="Firebase UID")
    email: str = Field(..., min_length=5, description="Email del usuario")
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    piano_level: PianoLevel = Field(..., description="Nivel de piano")
    
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email must contain @')
        return v.lower().strip()
    
    @validator('name')
    def validate_name(cls, v):
        return v.strip()


class UserResponseDTO(BaseModel):
    """DTO para respuesta de usuario"""
    uid: str
    email: str
    name: str
    piano_level: str
    
    class Config:
        from_attributes = True


class UpdateUserDTO(BaseModel):
    """DTO para actualizar usuario"""
    email: Optional[str] = Field(None, min_length=5, description="Email del usuario")
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="Nombre del usuario")
    piano_level: Optional[PianoLevel] = Field(None, description="Nivel de piano")
    
    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Email must contain @')
        return v.lower().strip() if v else v
    
    @validator('name')
    def validate_name(cls, v):
        return v.strip() if v else v