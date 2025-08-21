import logging
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
from app.domain.entities.user import User
from app.shared.utils import parse_piano_level

logger = logging.getLogger(__name__)


class RegisterUserUseCase:
    """Use case for registering a user"""

    def __init__(self, user_service: UserServiceInterface):
        self.user_service = user_service

    async def execute(self, create_user_dto: CreateUserDTO) -> UserResponseDTO:
        try:
            logger.info(f"Initiating user registration for UID: {create_user_dto.uid}")

            # Convert DTO -> Domain Entity
            user_entity = User(
                uid=create_user_dto.uid,
                email=create_user_dto.email,
                name=create_user_dto.name,
                piano_level=create_user_dto.piano_level
            ) 

            # Call domain service to persist user
            created_user = await self.user_service.create_user(user_entity)

            # Build response DTO (Entity -> DTO)
            user_response = UserResponseDTO(
                uid=created_user.uid,
                email=created_user.email,
                name=created_user.name,
                piano_level=created_user.piano_level.value
            )

            logger.info(f"User registered successfully: {created_user.uid}")
            return user_response

        except (UserAlreadyExistsException, InvalidUserDataException,
                DatabaseConnectionException, FirebaseAuthException,
                ValidationException) as e:
            logger.warning(f"Error registering user {create_user_dto.uid}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {create_user_dto.uid} - {str(e)}")
            raise UserServiceException(f"Unexpected error during registration: {str(e)}")
