from abc import ABC, abstractmethod
from app.domain.entities.auth import Auth
from app.domain.entities.login import Login
from app.domain.entities.token import Token

class AuthRepository(ABC):
    """Interface for implementation in infrastructure"""

    @abstractmethod
    async def register_user(self, email: str, password: str) -> Auth:
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> Login:
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> Token:
        pass