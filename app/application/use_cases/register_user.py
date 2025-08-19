from typing import Dict, Any
from app.application.interfaces.user_service_interface import AuthServiceInterface
from app.domain.services.auth_service import AuthDomainService
from app.application.dto.user_dto import CreateUserDTO, UserResponseDTO
from app.core.exceptions import (
    AuthServiceException, 
    UserAlreadyExistsException, 
    InvalidUserDataException,
    DatabaseConnectionException
)
import logging

logger = logging.getLogger(__name__)


class RegisterUserUseCase(AuthServiceInterface):
    """Use case for register user"""
    
    def __init__(self, auth_domain_service: AuthDomainService):
        self.auth_domain_service = auth_domain_service
    
    async def register_user(self, uid: str, email: str, name: str, piano_level) -> Dict[str, Any]:
        try:
            logger.info(f"Initiating user registration for UID: {uid}")
            
            # Validar datos de entrada usando DTO
            create_user_dto = CreateUserDTO(
                uid=uid,
                email=email,
                name=name,
                piano_level=piano_level
            )
            
            # Crear usuario usando el servicio de dominio
            created_user = await self.auth_domain_service.create_user(
                uid=create_user_dto.uid,
                email=create_user_dto.email,
                name=create_user_dto.name,
                piano_level=create_user_dto.piano_level
            )
            
            # Convertir a DTO de respuesta
            user_response = UserResponseDTO(
                uid=created_user.uid,
                email=created_user.email,
                name=created_user.name,
                piano_level=created_user.piano_level.value,
            )
            
            logger.info(f"User registered successfully: {uid}")
            return user_response.dict()
            
        except UserAlreadyExistsException:
            logger.warning(f"Attempt to register existing user: {uid}")
            raise
        except InvalidUserDataException:
            logger.warning(f"Invalid user data for registration: {uid}")
            raise
        except DatabaseConnectionException:
            logger.error(f"Database error during user registration: {uid}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during user registration: {uid} - {str(e)}")
            raise AuthServiceException(f"Unexpected error during registration: {str(e)}")
    
    async def get_user_profile(self, uid: str) -> Dict[str, Any]:
        try:
            logger.info(f"Getting user profile for UID: {uid}")
            
            user = await self.auth_domain_service.get_user_by_uid(uid)
            
            user_response = UserResponseDTO(
                uid=user.uid,
                email=user.email,
                name=user.name,
                piano_level=user.piano_level.value,
            )
            
            return user_response.dict()
            
        except Exception as e:
            logger.error(f"Error getting user profile: {uid} - {str(e)}")
            raise
    
    async def user_exists(self, uid: str) -> bool:
        try:
            return await self.auth_domain_service.user_exists(uid)
        except Exception as e:
            logger.error(f"Error checking user existence: {uid} - {str(e)}")
            raise