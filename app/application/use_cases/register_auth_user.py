from app.application.dto.auth_dto import AuthDTO
from app.core.exceptions import FirebaseAuthException, UserServiceException
import logging

from app.domain.services.auth_service import AuthService

logger = logging.getLogger(__name__)

class RegisterAuthUserUseCase:
    """Use case for registering user credentials in Firebase"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> AuthDTO:
        try:
            logger.info(f"Registering user in Firebase: {email}")
            auth_dto = await self.auth_service.register_user(email, password)
            logger.info(f"User registered successfully in Firebase: {auth_dto.uid}")
            return auth_dto
        except FirebaseAuthException as e:
            logger.warning(f"Firebase error creating user: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating Firebase user: {str(e)}")
            raise UserServiceException(f"Unexpected error creating Firebase user: {str(e)}")
