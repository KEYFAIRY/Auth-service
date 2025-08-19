from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel
from app.infrastructure.database.mysql_connection import db_connection
from app.core.exceptions import DatabaseConnectionException, UserAlreadyExistsException, UserNotFoundException
from app.shared.enums import PianoLevel
import logging

logger = logging.getLogger(__name__)


class MySQLUserRepository(UserRepository):
    """Concrete implementation of the user repository using MySQL"""

    async def create_user(self, user: User) -> User:
        """Create a new user in the database"""
        async with db_connection.get_async_session() as session:
            try:
                # Create database model
                user_model = UserModel(
                    uid=user.uid,
                    email=user.email,
                    name=user.name,
                    piano_level=user.piano_level
                )

                # Add to session
                session.add(user_model)
                await session.commit()
                await session.refresh(user_model)

                # Convert back to domain entity
                created_user = self._model_to_entity(user_model)
                logger.info(f"User created successfully: {created_user.uid}")
                return created_user

            except IntegrityError as e:
                await session.rollback()
                logger.error(f"Integrity error creating user: {e}")
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
            except Exception as e:
                await session.rollback()
                logger.error(f"Unexpected error creating user: {e}")
                raise DatabaseConnectionException(f"Unexpected error creating user: {str(e)}")

    async def get_user_by_uid(self, uid: str) -> Optional[User]:
        """Get user by UID"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.uid == uid)
                )
                user_model = result.scalar_one_or_none()

                if user_model:
                    return self._model_to_entity(user_model)
                return None

            except SQLAlchemyError as e:
                logger.error(f"Database error getting user by UID: {e}")
                raise DatabaseConnectionException(f"Error getting user: {str(e)}")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.email == email.lower())
                )
                user_model = result.scalar_one_or_none()

                if user_model:
                    return self._model_to_entity(user_model)
                return None

            except SQLAlchemyError as e:
                logger.error(f"Database error getting user by email: {e}")
                raise DatabaseConnectionException(f"Error getting user: {str(e)}")

    async def user_exists_by_uid(self, uid: str) -> bool:
        """Check if a user exists by UID"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel.uid).where(UserModel.uid == uid)
                )
                return result.scalar_one_or_none() is not None

            except SQLAlchemyError as e:
                logger.error(f"Database error checking user existence by UID: {e}")
                raise DatabaseConnectionException(f"Error checking user existence: {str(e)}")

    async def user_exists_by_email(self, email: str) -> bool:
        """Check if a user exists by email"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel.email).where(UserModel.email == email.lower())
                )
                return result.scalar_one_or_none() is not None

            except SQLAlchemyError as e:
                logger.error(f"Database error checking user existence by email: {e}")
                raise DatabaseConnectionException(f"Error checking user existence: {str(e)}")

    async def update_user(self, user: User) -> User:
        """Update user"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.uid == user.uid)
                )
                user_model = result.scalar_one_or_none()

                if not user_model:
                    raise UserNotFoundException(f"User with UID {user.uid} not found")

                # Update fields
                user_model.email = user.email
                user_model.name = user.name
                user_model.piano_level = user.piano_level

                await session.commit()
                await session.refresh(user_model)

                return self._model_to_entity(user_model)

            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Database error updating user: {e}")
                raise DatabaseConnectionException(f"Error updating user: {str(e)}")

    async def delete_user(self, uid: str) -> bool:
        """Delete user"""
        async with db_connection.get_async_session() as session:
            try:
                result = await session.execute(
                    select(UserModel).where(UserModel.uid == uid)
                )
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
        """Convert database model to domain entity"""
        return User(
            uid=user_model.uid,
            email=user_model.email,
            name=user_model.name,
            piano_level=user_model.piano_level
        )