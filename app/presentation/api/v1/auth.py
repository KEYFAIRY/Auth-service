from fastapi import APIRouter, Depends, status
from app.presentation.schemas.auth_schema import (
    RegisterAuthRequest, 
    LoginRequest, 
    RefreshTokenRequest,
    AuthResponse,
    LoginResponse,
    TokenResponse
)
from app.presentation.schemas.common_schema import StandardResponse
from app.application.use_cases.register_auth_user import RegisterAuthUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.application.use_cases.refresh_token import RefreshTokenUseCase
from app.presentation.api.dependencies import (
    register_auth_user_use_case_dependency,
    login_user_use_case_dependency,
    refresh_token_use_case_dependency
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user credentials",
    description="Register a new user in Firebase Authentication"
)
async def register_auth_user(
    auth_request: RegisterAuthRequest,
    register_auth_use_case: RegisterAuthUserUseCase = Depends(register_auth_user_use_case_dependency)
):
    logger.info(f"Registering user credentials for: {auth_request.email}")
    
    # Execute use case
    auth_dto = await register_auth_use_case.execute(
        email=auth_request.email,
        password=auth_request.password
    )
    
    # Create response data
    auth_response = AuthResponse(
        uid=auth_dto.uid,
        email=auth_dto.email
    )
    
    # Return standardized response
    response = StandardResponse.created(
        data=auth_response.dict(),
        message="User credentials registered successfully"
    )
    
    logger.info(f"User credentials registered successfully: {auth_dto.uid}")
    return response


@router.post(
    "/login",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate user and return access tokens"
)
async def login_user(
    login_request: LoginRequest,
    login_use_case: LoginUserUseCase = Depends(login_user_use_case_dependency)
):
    logger.info(f"Logging in user: {login_request.email}")
    
    # Execute use case
    login_dto = await login_use_case.execute(
        email=login_request.email,
        password=login_request.password
    )
    
    # Create response data
    login_response = LoginResponse(
        uid=login_dto.uid,
        email=login_dto.email,
        id_token=login_dto.id_token,
        refresh_token=login_dto.refresh_token
    )
    
    # Return standardized response
    response = StandardResponse.success(
        data=login_response.dict(),
        message="User logged in successfully"
    )
    
    logger.info(f"User logged in successfully: {login_dto.uid}")
    return response


@router.post(
    "/refresh-token",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Refresh the user's access token using refresh token"
)
async def refresh_token(
    token_request: RefreshTokenRequest,
    refresh_token_use_case: RefreshTokenUseCase = Depends(refresh_token_use_case_dependency)
):
    logger.info("Refreshing user token")
    
    # Execute use case
    token_dto = await refresh_token_use_case.execute(
        refresh_token=token_request.refresh_token
    )
    
    # Create response data
    token_response = TokenResponse(
        id_token=token_dto.id_token,
        refresh_token=token_dto.refresh_token
    )
    
    # Return standardized response
    response = StandardResponse.success(
        data=token_response.dict(),
        message="Token refreshed successfully"
    )
    
    logger.info("Token refreshed successfully")
    return response