from abc import ABC, abstractmethod
from typing import Dict, Any
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO
from app.shared.enums import PianoLevel


class UserServiceInterface(ABC):
    """Interface for the user service in the application layer"""

    @abstractmethod
    async def register_user(self, new_user: CreateUserDTO) -> UserResponseDTO:
        """Register a new user"""
        pass
    
    @abstractmethod
    async def update_user(self, uid: str, new_user: UpdateUserDTO) -> UserResponseDTO:
        """Register a new user"""
        pass
    
    @abstractmethod
    async def get_user_by_uid(self, uid: str) -> UserResponseDTO:
        """Get user profile"""
        pass
    
    @abstractmethod
    async def user_exists(self, uid: str) -> bool:
        """Check if a user exists"""
        pass