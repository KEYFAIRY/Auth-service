import logging
from app.application.dto.user_dto import UpdateUserDTO, UserResponseDTO
from app.core.exceptions import DatabaseConnectionException, InvalidUserDataException, UserNotFoundException, UserServiceException
from app.domain.services.user_service import UserService

logger = logging.getLogger(__name__)

class UpdateUserUseCase:
    """Use case for updating a user"""

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def execute(self, uid: str, update_user_dto: UpdateUserDTO) -> UserResponseDTO:
        try:
            logger.info(f"Updating user with UID: {uid}")

            updated_user = await self.user_service.update_user(uid, update_user_dto)

            user_response = UserResponseDTO(
                uid=updated_user.uid,
                email=updated_user.email,
                name=updated_user.name,
                piano_level=updated_user.piano_level.value
            )

            logger.info(f"User updated successfully: {uid}")
            return user_response

        except (UserNotFoundException, InvalidUserDataException, DatabaseConnectionException) as e:
            logger.warning(f"Error updating user {uid}: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user update: {uid} - {str(e)}")
            raise UserServiceException(f"Unexpected error during update: {str(e)}")
