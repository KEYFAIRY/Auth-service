from typing import List
from app.application.dto.user_dto import UserResponseDTO
from app.core.exceptions import (
    UserNotFoundException,
    DatabaseConnectionException,
    UserServiceException,
    ValidationException,
)
import logging

from app.shared.utils import parse_piano_level
from app.domain.services.user_service import UserService

logger = logging.getLogger(__name__)


class GetUserUseCase:
    """Use case for retrieving users"""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def get_by_id(self, uid: str) -> UserResponseDTO:
        try:
            logger.info(f"Fetching user with UID: {uid}")

            user = await self.user_service.get_user_by_uid(uid)
            if not user:
                raise UserNotFoundException(f"User with UID {uid} not found")

            piano_level_value = parse_piano_level(user.piano_level)

            user_response = UserResponseDTO(
                uid=user.uid,
                email=user.email,
                name=user.name,
                piano_level=piano_level_value,
            )

            logger.info(f"User retrieved successfully: {uid}")
            return user_response

        except (UserNotFoundException, DatabaseConnectionException, ValidationException) as e:
            logger.warning(f"Error fetching user {uid}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching user: {uid} - {str(e)}")
            raise UserServiceException(f"Unexpected error fetching user: {str(e)}")

    async def get_all(self) -> List[UserResponseDTO]:
        try:
            logger.info("Fetching all users")

            users = await self.user_service.get_all_users()

            user_responses = [
                UserResponseDTO(
                    uid=user.uid,
                    email=user.email,
                    name=user.name,
                    piano_level=parse_piano_level(user.piano_level),
                )
                for user in users
            ]

            logger.info(f"Retrieved {len(user_responses)} users successfully")
            return user_responses

        except (DatabaseConnectionException, ValidationException) as e:
            logger.warning(f"Error fetching all users: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching all users: {str(e)}")
            raise UserServiceException(f"Unexpected error fetching all users: {str(e)}")
