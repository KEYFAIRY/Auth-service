# app/application/use_cases/register_user.py
from app.application.interfaces.user_service_interface import UserServiceInterface
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidUserDataException,
    DatabaseConnectionException,
    FirebaseAuthException,
    ValidationException,
    UserServiceException
)
import logging

from app.shared.utils import parse_piano_level

logger = logging.getLogger(__name__)


class RegisterUserUseCase:
    """Use case for registering a user"""

    def __init__(self, user_service: UserServiceInterface):
        self.user_service = user_service

    async def execute(self, create_user_dto: CreateUserDTO) -> UserResponseDTO:
        try:
            logger.info(f"Initiating user registration for UID: {create_user_dto.uid}")

            # Create user using the application service
            created_user = await self.user_service.create_user(create_user_dto)

            # Convert piano level safely
            piano_level_value = parse_piano_level(created_user.piano_level)

            # Convert to response DTO
            user_response = UserResponseDTO(
                uid=created_user.uid,
                email=created_user.email,
                name=created_user.name,
                piano_level=piano_level_value,
            )

            logger.info(f"User registered successfully: {create_user_dto.uid}")
            return user_response

        except (UserAlreadyExistsException, InvalidUserDataException,
                DatabaseConnectionException, FirebaseAuthException,
                ValidationException) as e:
            # Already a UserServiceException subclass
            logger.warning(f"Error registering user {create_user_dto.uid}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {create_user_dto.uid} - {str(e)}")
            raise UserServiceException(f"Unexpected error during registration: {str(e)}")