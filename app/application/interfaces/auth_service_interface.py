from abc import ABC, abstractmethod
from typing import Dict
from app.application.dto.user_dto import UpdateUserDTO
from app.shared.enums import PianoLevel


class AuthServiceInterface(ABC):
    """Interface for the authentication service in the application layer"""

    @abstractmethod
    async def register_user(self, uid: str, email: str, name: str, piano_level: PianoLevel) -> Dict[str, Any]:
        """Register a new user"""
        pass

    @abstractmethod
    async def get_user_profile(self, uid: str) -> Dict[str, Any]:
        """Get user profile"""
        pass

    @abstractmethod
    async def user_exists(self, uid: str) -> bool:
        """Check if a user exists"""
        pass