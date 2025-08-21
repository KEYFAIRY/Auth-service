from pydantic import BaseModel

class AuthDTO(BaseModel):
    uid: str
    email: str

class LoginDTO(BaseModel):
    uid: str
    email: str
    id_token: str
    refresh_token: str

class TokenDTO(BaseModel):
    id_token: str
    refresh_token: str