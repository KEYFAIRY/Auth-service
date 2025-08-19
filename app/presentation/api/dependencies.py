from functools import lru_cache
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.domain.services.auth_service import AuthDomainService
from app.application.use_cases.register_user import RegisterUserUseCase


@lru_cache()
def get_user_repository() -> MySQLUserRepository:
    """Obtener instancia del repositorio de usuarios"""
    return MySQLUserRepository()


@lru_cache()
def get_auth_domain_service() -> AuthDomainService:
    """Obtener instancia del servicio de dominio de autenticación"""
    user_repository = get_user_repository()
    return AuthDomainService(user_repository)


@lru_cache()
def get_register_user_use_case() -> RegisterUserUseCase:
    """Obtener instancia del caso de uso de registro de usuario"""
    auth_domain_service = get_auth_domain_service()
    return RegisterUserUseCase(auth_domain_service)


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