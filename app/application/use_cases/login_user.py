# app/application/use_cases/login_user.py
from app.application.dto.auth_dto import LoginDTO
from app.domain.services.auth_service import AuthService
from app.core.exceptions import FirebaseAuthException, UserServiceException
import logging

logger = logging.getLogger(__name__)


class LoginUserUseCase:
    """Use case for logging in a user via Firebase"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> LoginDTO:
        try:
            logger.info(f"Logging in user: {email}")

            # llamamos al dominio
            login_entity = await self.auth_service.login(email, password)

            # convertir de entidad de dominio → DTO de aplicación
            login_dto = LoginDTO(
                uid=login_entity.uid,
                email=login_entity.email,
                id_token=login_entity.id_token,
                refresh_token=login_entity.refresh_token,
            )

            logger.info(f"User logged in successfully: {email}")
            return login_dto

        except FirebaseAuthException as e:
            logger.warning(f"Firebase login failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error logging in user {email}: {str(e)}")
            raise UserServiceException(f"Unexpected error logging in user {email}: {str(e)}")
