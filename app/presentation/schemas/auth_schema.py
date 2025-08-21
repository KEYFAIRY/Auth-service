from pydantic import BaseModel, Field, EmailStr


class RegisterAuthRequest(BaseModel):
    """Esquema para registrar usuario en Auth"""
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
    """Esquema para login"""
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
    """Esquema para refrescar token"""
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
