from app.application.interfaces.auth_service_interface import AuthInterface
from app.application.dto.auth_dto import LoginDTO
from app.core.exceptions import FirebaseAuthException, UserServiceException
import logging

logger = logging.getLogger(__name__)

class LoginUserUseCase:
    """Use case for logging in a user via Firebase"""

    def __init__(self, auth_service: AuthInterface):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> LoginDTO:
        try:
            logger.info(f"Logging in user: {email}")
            login_dto = await self.auth_service.login(email, password)
            logger.info(f"User logged in successfully: {email}")
            return login_dto
        except FirebaseAuthException as e:
            logger.warning(f"Firebase login failed: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error logging in user {email}: {str(e)}")
            raise UserServiceException(f"Unexpected error logging in user {email}: {str(e)}")
