from pydantic import BaseModel, Field, EmailStr


class RegisterAuthRequest(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")

    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "strongpassword123"
            }
        }


class LoginRequest(BaseModel):
    """Schema for login"""
    email: EmailStr = Field(..., description="Email del usuario")
    password: str = Field(..., min_length=6, description="Contraseña del usuario")

    class Config:
        schema_extra = {
            "example": {
                "email": "usuario@example.com",
                "password": "strongpassword123"
            }
        }


class RefreshTokenRequest(BaseModel):
    """Schema for refreshing token"""
    refresh_token: str = Field(..., description="Refresh token del usuario")

    class Config:
        schema_extra = {
            "example": {
                "refresh_token": "REFRESH_TOKEN_VALUE"
            }
        }


class AuthResponse(BaseModel):
    uid: str
    email: str


class LoginResponse(BaseModel):
    uid: str
    email: str
    id_token: str
    refresh_token: str


class TokenResponse(BaseModel):
    id_token: str
    refresh_token: str
