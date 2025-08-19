from fastapi import APIRouter, Depends, HTTPException, status
from app.presentation.schemas.user_schema import CreateUserRequest, UserResponse
from app.presentation.schemas.common_schema import StandardResponse
from app.application.use_cases.register_user import RegisterUserUseCase
from app.presentation.api.dependencies import register_user_use_case_dependency
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidUserDataException,
    DatabaseConnectionException,
    AuthServiceException
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with the provided information",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "code": "201",
                        "message": "User created successfully",
                        "data": {
                            "uid": "firebase_uid_123",
                            "email": "usuario@example.com",
                            "name": "Juan Pérez",
                            "piano_level": "beginner",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad request - Invalid input data",
            "content": {
                "application/json": {
                    "example": {
                        "code": "400",
                        "message": "Validation errors: email: Invalid email format",
                        "data": None
                    }
                }
            }
        },
        409: {
            "description": "Conflict - User already exists",
            "content": {
                "application/json": {
                    "example": {
                        "code": "409",
                        "message": "User with email usuario@example.com already exists",
                        "data": None
                    }
                }
            }
        },
        422: {
            "description": "Unprocessable Entity - Invalid user data",
            "content": {
                "application/json": {
                    "example": {
                        "code": "422",
                        "message": "Invalid user data: Name must be at least 2 characters long",
                        "data": None
                    }
                }
            }
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {
                        "code": "500",
                        "message": "Internal server error",
                        "data": None
                    }
                }
            }
        }
    }
)
async def create_user(
    user_request: CreateUserRequest,
    register_use_case: RegisterUserUseCase = Depends(register_user_use_case_dependency)
):

    try:
        logger.info(f"Creating user with UID: {user_request.uid}")
        
        # Ejecutar caso de uso
        user_data = await register_use_case.register_user(
            uid=user_request.uid,
            email=user_request.email,
            name=user_request.name,
            piano_level=user_request.piano_level
        )
        
        # Crear respuesta exitosa
        response = StandardResponse.created(
            data=user_data,
            message="User created successfully"
        )
        
        logger.info(f"User created successfully: {user_request.uid}")
        return response
        
    except UserAlreadyExistsException as e:
        logger.warning(f"User already exists: {user_request.uid}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=StandardResponse.conflict(e.message).dict()
        )
    
    except InvalidUserDataException as e:
        logger.warning(f"Invalid user data: {user_request.uid} - {e.message}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=StandardResponse.error(e.message, "422").dict()
        )
    
    except DatabaseConnectionException as e:
        logger.error(f"Database error creating user: {user_request.uid} - {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=StandardResponse.internal_error("Database connection error").dict()
        )
    
    except AuthServiceException as e:
        logger.error(f"Auth service error: {user_request.uid} - {e.message}")
        status_code = _get_http_status_from_code(e.code)
        raise HTTPException(
            status_code=status_code,
            detail=StandardResponse.error(e.message, e.code).dict()
        )
    
    except Exception as e:
        logger.error(f"Unexpected error creating user: {user_request.uid} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=StandardResponse.internal_error("An unexpected error occurred").dict()
        )


@router.get(
    "/{uid}",
    response_model=StandardResponse,
    summary="Get user profile",
    description="Retrieve user profile information by UID",
    responses={
        200: {
            "description": "User profile retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "code": "200",
                        "message": "Success",
                        "data": {
                            "uid": "firebase_uid_123",
                            "email": "usuario@example.com",
                            "name": "Juan Pérez",
                            "piano_level": "beginner",
                            "created_at": "2024-01-15T10:30:00Z",
                            "updated_at": "2024-01-15T10:30:00Z"
                        }
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "code": "404",
                        "message": "User not found",
                        "data": None
                    }
                }
            }
        }
    }
)
async def get_user(
    uid: str,
    register_use_case: RegisterUserUseCase = Depends(register_user_use_case_dependency)
):

    try:
        logger.info(f"Getting user profile for UID: {uid}")
        
        user_data = await register_use_case.get_user_profile(uid)
        
        response = StandardResponse.success(
            data=user_data,
            message="User profile retrieved successfully"
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Error getting user profile: {uid} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=StandardResponse.not_found("User not found").dict()
        )


def _get_http_status_from_code(error_code: str) -> int:
    """Mapear código de error a código HTTP"""
    code_mapping = {
        "200": 200, "201": 201, "202": 202,
        "400": 400, "401": 401, "403": 403,
        "404": 404, "409": 409, "422": 422,
        "500": 500, "503": 503
    }
    return code_mapping.get(error_code, 500)