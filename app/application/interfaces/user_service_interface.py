from abc import ABC, abstractmethod
from typing import List
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO, UserResponseDTO


class UserServiceInterface(ABC):
    """Interface for the user service in the application layer"""

    @abstractmethod
    async def create_user(self, new_user: CreateUserDTO) -> UserResponseDTO:
        """Create a new user"""
        pass

    @abstractmethod
    async def update_user(self, uid: str, updated_user: UpdateUserDTO) -> UserResponseDTO:
        """Update an existing user by UID"""
        pass

    @abstractmethod
    async def get_user_by_uid(self, uid: str) -> UserResponseDTO:
        """Get a user profile by UID"""
        pass

    @abstractmethod
    async def get_all_users(self) -> List[UserResponseDTO]:
        """Get all users"""
        pass

    @abstractmethod
    async def delete_user(self, uid: str) -> None:
        """Delete a user by UID"""
        pass

    @abstractmethod
    async def user_exists(self, uid: str) -> bool:
        """Check if a user exists"""
        pass
