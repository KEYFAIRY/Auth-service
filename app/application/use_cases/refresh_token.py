from app.application.dto.auth_dto import TokenDTO
from app.core.exceptions import FirebaseAuthException, UserServiceException
import logging

from app.domain.services.auth_service import AuthService

logger = logging.getLogger(__name__)

class RefreshTokenUseCase:
    """Use case for refreshing a Firebase token"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, refresh_token: str) -> TokenDTO:
        try:
            logger.info("Refreshing Firebase token")
            token_dto = await self.auth_service.refresh_token(refresh_token)
            logger.info("Firebase token refreshed successfully")
            return token_dto
        except FirebaseAuthException as e:
            logger.warning(f"Firebase token refresh failed: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error refreshing token: {str(e)}")
            raise UserServiceException(f"Unexpected error refreshing token: {str(e)}")
