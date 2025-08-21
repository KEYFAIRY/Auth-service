from functools import lru_cache
from app.application.use_cases.get_user import GetUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.refresh_token import RefreshTokenUseCase
from app.application.use_cases.register_auth_user import RegisterAuthUserUseCase
from app.domain.services.auth_service import AuthService
from app.infrastructure.repositories.firebase_auth_repository import FirebaseAuthRepository
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.domain.services.user_service import UserService
from app.application.use_cases.register_user import RegisterUserUseCase

# Repositorios

@lru_cache()
def get_user_repository() -> MySQLUserRepository:
    """Obtener instancia del repositorio de usuarios"""
    return MySQLUserRepository()

@lru_cache()
def get_auth_repository() -> FirebaseAuthRepository:
    """Obtener instancia del repositorio de autenticacion"""
    return FirebaseAuthRepository()


# Servicios

@lru_cache()
def get_user_domain_service() -> UserService:
    """Obtener instancia del servicio de dominio de usuario"""
    user_repository = get_user_repository()
    return UserService(user_repository)

@lru_cache()
def get_auth_domain_service() -> AuthService:
    """Obtener instancia del servicio de dominio de autenticación"""
    auth_repository = get_auth_repository()
    return AuthService(auth_repository)


# Casos de uso

@lru_cache()
def get_register_user_use_case() -> RegisterUserUseCase:
    """Obtener instancia del caso de uso de registro de usuario"""
    user_service = get_user_domain_service()
    return RegisterUserUseCase(user_service)

@lru_cache()
def get_get_user_use_case() -> GetUserUseCase:
    """Obtener instancia del caso de uso de obtención de usuario"""
    user_service = get_user_domain_service()
    return GetUserUseCase(user_service)

@lru_cache()
def get_login_user_use_case() -> LoginUserUseCase:
    """Obtener instancia del caso de uso de inicio de sesión de usuario"""
    auth_service = get_auth_domain_service()
    return LoginUserUseCase(auth_service)

@lru_cache()
def get_register_auth_user_use_case() -> RegisterAuthUserUseCase:
    """Obtener instancia del caso de uso de registro de usuario"""
    auth_service = get_auth_domain_service()
    return RegisterAuthUserUseCase(auth_service)

@lru_cache()
def get_refresh_token_use_case() -> RefreshTokenUseCase:
    """Obtener instancia del caso de uso de refresco de token"""
    auth_service = get_auth_domain_service()
    return RefreshTokenUseCase(auth_service)


# Funciones de dependencia para FastAPI

# Repositorios

def user_repository_dependency():
    """Dependencia para inyectar repositorio de usuarios"""
    return get_user_repository()

def auth_repository_dependency():
    """Dependencia para inyectar repositorio de autenticación"""
    return get_auth_repository()

# Servicios

def user_domain_service_dependency():
    """Dependencia para inyectar servicio de dominio"""
    return get_user_domain_service()

def auth_domain_service_dependency():
    """Dependencia para inyectar servicio de dominio de autenticación"""
    return get_auth_domain_service()

# Casos de uso

def register_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de registro"""
    return get_register_user_use_case()

def get_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de obtención de usuario"""
    return get_get_user_use_case()

def login_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de inicio de sesión de usuario"""
    return get_login_user_use_case()

def register_auth_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de registro de usuario"""
    return get_register_auth_user_use_case()

def refresh_token_use_case_dependency():
    """Dependencia para inyectar caso de uso de refresco de token"""
    return get_refresh_token_use_case()