from functools import lru_cache
from app.application.use_cases.get_user import GetUserUseCase
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.domain.services.user_service import UserService
from app.application.use_cases.register_user import RegisterUserUseCase

# Repositorios

@lru_cache()
def get_user_repository() -> MySQLUserRepository:
    """Obtener instancia del repositorio de usuarios"""
    return MySQLUserRepository()


# Servicios

@lru_cache()
def get_user_domain_service() -> UserService:
    """Obtener instancia del servicio de dominio de autenticación"""
    user_repository = get_user_repository()
    return UserService(user_repository)


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


# Funciones de dependencia para FastAPI
def user_repository_dependency():
    """Dependencia para inyectar repositorio de usuarios"""
    return get_user_repository()

def auth_domain_service_dependency():
    """Dependencia para inyectar servicio de dominio"""
    return get_auth_domain_service()

def register_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de registro"""
    return get_register_user_use_case()

def get_user_use_case_dependency():
    """Dependencia para inyectar caso de uso de obtención de usuario"""
    return get_get_user_use_case()