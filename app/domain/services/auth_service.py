from app.domain.entities.auth import Auth
from app.domain.entities.login import Login
from app.domain.entities.token import Token
from app.domain.repositories.auth_repository import AuthRepository
from app.core.exceptions import (
    FirebaseAuthException,
    InvalidUserDataException,
    UserAlreadyExistsException,
    UserNotFoundException,
)


class AuthService:
    """Domain service for authentication business logic"""

    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    async def register_user(self, email: str, password: str) -> Auth:
        self._validate_credentials(email, password)

        try:
            # Create user in Firebase Auth
            auth_entity = await self.auth_repository.register_user(email, password)
            return auth_entity
        except UserAlreadyExistsException: 
            raise
        except Exception as e:
            raise FirebaseAuthException(str(e))

    async def login(self, email: str, password: str) -> Login:
        self._validate_credentials(email, password)

        try:
            login_entity = await self.auth_repository.login(email, password)
            if not login_entity:
                raise UserNotFoundException("User not found or invalid credentials")
            return login_entity
        except Exception as e:
            raise FirebaseAuthException(str(e))

    async def refresh_token(self, refresh_token: str) -> Token:
        if not refresh_token or len(refresh_token.strip()) == 0:
            raise InvalidUserDataException("Refresh token is required")

        try:
            token_entity = await self.auth_repository.refresh_token(refresh_token)
            return token_entity
        except Exception as e:
            raise FirebaseAuthException(str(e))

    def _validate_credentials(self, email: str, password: str):
        """Validación mínima de email y password"""
        if not email or "@" not in email:
            raise InvalidUserDataException("Invalid email format")
        if not password or len(password) < 6:
            raise InvalidUserDataException("Password must be at least 6 characters long")
