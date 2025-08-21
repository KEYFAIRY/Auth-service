from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.user import User


class UserRepository(ABC):
    """Interface for the user repository"""

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def get_user_by_uid(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        """Get all users"""
        pass

    @abstractmethod
    async def user_exists_by_uid(self, uid: str) -> bool:
        """Check if a user exists by UID"""
        pass

    @abstractmethod
    async def user_exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email"""
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """Update user"""
        pass

    @abstractmethod
    async def delete_user(self, uid: str) -> bool:
        """Delete user"""
        pass
