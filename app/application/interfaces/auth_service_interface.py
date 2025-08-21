from abc import ABC, abstractmethod
from app.application.dto.auth_dto import AuthDTO, LoginDTO, TokenDTO

class AuthInterface(ABC):
    """Application-level interface for authentication use cases"""

    @abstractmethod
    async def register_user(self, email: str, password: str) -> AuthDTO:
        """Create user credentials in Firebase"""
        pass

    @abstractmethod
    async def login(self, email: str, password: str) -> LoginDTO:
        """Login user and return Firebase token"""
        pass

    @abstractmethod
    async def refresh_token(self, refresh_token: str) -> TokenDTO:
        """Refresh Firebase token"""
        pass
