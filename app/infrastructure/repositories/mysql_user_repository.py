from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.database.mysql_connection import db_connection
from app.core.exceptions import (
    DatabaseConnectionException,
    InvalidUserDataException,
    UserAlreadyExistsException,
    UserNotFoundException
)
import logging

from app.shared.enums import PianoLevel

logger = logging.getLogger(__name__)


class MySQLUserRepository(UserRepository):
    """Concrete implementation of the user repository using MySQL"""

    async def create_user(self, user: User) -> User:
        async with db_connection.get_async_session() as session:
            try:
                user_model = UserModel(
                    uid=user.uid,
                    email=user.email.lower(),
                    name=user.name.strip(),
                    piano_level=user.piano_level.value
                )
                session.add(user_model)
                await session.commit()
                await session.refresh(user_model)
                return self._model_to_entity(user_model)

            except IntegrityError as e:
                await session.rollback()
                if "uid" in str(e):
                    raise UserAlreadyExistsException(f"User with UID {user.uid} already exists")
                elif "email" in str(e):
                    raise UserAlreadyExistsException(f"User with email {user.email} already exists")
                else:
                    raise UserAlreadyExistsException("User already exists")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error creating user: {e}")
                raise DatabaseConnectionException(f"Error creating user: {str(e)}")

    async def get_user_by_uid(self, uid: str) -> Optional[User]:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel).where(UserModel.uid == uid))
                user_model = result.scalar_one_or_none()
                return self._model_to_entity(user_model) if user_model else None
            except SQLAlchemyError as e:
                logger.error(f"Database error getting user by UID: {e}")
                raise DatabaseConnectionException(f"Error getting user by UID: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel).where(UserModel.email == email.lower()))
                user_model = result.scalar_one_or_none()
                return self._model_to_entity(user_model) if user_model else None
            except SQLAlchemyError as e:
                logger.error(f"Database error getting user by email: {e}")
                raise DatabaseConnectionException(f"Error getting user by email: {str(e)}")

    async def get_all_users(self) -> List[User]:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel))
                users = result.scalars().all()
                return [self._model_to_entity(u) for u in users]
            except SQLAlchemyError as e:
                logger.error(f"Database error getting all users: {e}")
                raise DatabaseConnectionException(f"Error getting all users: {str(e)}")

    async def user_exists_by_uid(self, uid: str) -> bool:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel.uid).where(UserModel.uid == uid))
                return result.scalar_one_or_none() is not None
            except SQLAlchemyError as e:
                logger.error(f"Database error checking user existence by UID: {e}")
                raise DatabaseConnectionException(f"Error checking user existence by UID: {str(e)}")

    async def user_exists_by_email(self, email: str) -> bool:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel.email).where(UserModel.email == email.lower()))
                return result.scalar_one_or_none() is not None
            except SQLAlchemyError as e:
                logger.error(f"Database error checking user existence by email: {e}")
                raise DatabaseConnectionException(f"Error checking user existence by email: {str(e)}")

    async def update_user(self, user: User) -> User:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel).where(UserModel.uid == user.uid))
                user_model = result.scalar_one_or_none()
                if not user_model:
                    raise UserNotFoundException(f"User with UID {user.uid} not found")

                user_model.email = user.email.lower()
                user_model.name = user.name.strip()
                user_model.piano_level = user.piano_level.value

                await session.commit()
                await session.refresh(user_model)
                return self._model_to_entity(user_model)
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error updating user: {e}")
                raise DatabaseConnectionException(f"Error updating user: {str(e)}")

    async def delete_user(self, uid: str) -> bool:
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(select(UserModel).where(UserModel.uid == uid))
                user_model = result.scalar_one_or_none()
                if not user_model:
                    return False

                await session.delete(user_model)
                await session.commit()
                return True
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error deleting user: {e}")
                raise DatabaseConnectionException(f"Error deleting user: {str(e)}")

    def _model_to_entity(self, user_model: UserModel) -> User:
        try:
            piano_level_enum = PianoLevel(user_model.piano_level)
        except ValueError:
            raise InvalidUserDataException("Valid piano level is required")
        
        return User(
            uid=user_model.uid,
            email=user_model.email,
            name=user_model.name,
            piano_level=piano_level_enum
    )