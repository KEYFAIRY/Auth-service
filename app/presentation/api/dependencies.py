from functools import lru_cache
from app.application.use_cases.get_user import GetUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.refresh_token import RefreshTokenUseCase
from app.application.use_cases.register_auth_user import RegisterAuthUserUseCase
from app.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.domain.services.auth_service import AuthService
from app.infrastructure.repositories.firebase_auth_repository import FirebaseAuthRepository
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.domain.services.user_service import UserService
from app.application.use_cases.register_user import RegisterUserUseCase

# Repositories
@lru_cache()
def get_user_repository() -> MySQLUserRepository:
    """Get user repository instance"""
    return MySQLUserRepository()

@lru_cache()
def get_auth_repository() -> FirebaseAuthRepository:
    """Get auth repository instance"""
    return FirebaseAuthRepository()


# Services
@lru_cache()
def get_user_domain_service() -> UserService:
    """Get user domain service instance"""
    user_repository = get_user_repository()
    return UserService(user_repository)

@lru_cache()
def get_auth_domain_service() -> AuthService:
    """Get auth domain service instance"""
    auth_repository = get_auth_repository()
    return AuthService(auth_repository)


# Use cases
@lru_cache()
def get_register_user_use_case() -> RegisterUserUseCase:
    """Get register user use case instance"""
    user_service = get_user_domain_service()
    return RegisterUserUseCase(user_service)

@lru_cache()
def get_get_user_use_case() -> GetUserUseCase:
    """Get user use case instance"""
    user_service = get_user_domain_service()
    return GetUserUseCase(user_service)

@lru_cache()
def get_login_user_use_case() -> LoginUserUseCase:
    """Get login user use case instance"""
    auth_service = get_auth_domain_service()
    return LoginUserUseCase(auth_service)

@lru_cache()
def get_register_auth_user_use_case() -> RegisterAuthUserUseCase:
    """Get register auth user use case instance"""
    auth_service = get_auth_domain_service()
    return RegisterAuthUserUseCase(auth_service)

@lru_cache()
def get_refresh_token_use_case() -> RefreshTokenUseCase:
    """Get refresh token use case instance"""
    auth_service = get_auth_domain_service()
    return RefreshTokenUseCase(auth_service)

@lru_cache()
def get_update_user_use_case() -> UpdateUserUseCase:
    """Get update user use case instance"""
    user_service = get_user_domain_service()
    return UpdateUserUseCase(user_service)


# Dependency functions for FastAPI

# Repositories
def user_repository_dependency():
    """Get user repository instance"""
    return get_user_repository()

def auth_repository_dependency():
    """Get auth repository instance"""
    return get_auth_repository()

# Services
def user_domain_service_dependency():
    """Get user domain service instance"""
    return get_user_domain_service()

def auth_domain_service_dependency():
    """Get auth domain service instance"""
    return get_auth_domain_service()

# Use cases
def register_user_use_case_dependency():
    """Get register user use case instance"""
    return get_register_user_use_case()

def get_user_use_case_dependency():
    """Get user use case instance"""
    return get_get_user_use_case()

def login_user_use_case_dependency():
    """Get login user use case instance"""
    return get_login_user_use_case()

def register_auth_user_use_case_dependency():
    """Get register auth user use case instance"""
    return get_register_auth_user_use_case()

def refresh_token_use_case_dependency():
    """Get refresh token use case instance"""
    return get_refresh_token_use_case()

def update_user_use_case_dependency():
    """Get update user use case instance"""
    return get_update_user_use_case()