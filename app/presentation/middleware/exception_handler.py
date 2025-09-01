from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    UserServiceException,
    UserAlreadyExistsException,
    InvalidUserDataException,
    UserNotFoundException,
    DatabaseConnectionException,
    FirebaseAuthException,
    ValidationException
)
from app.presentation.schemas.common_schema import StandardResponse
import logging

logger = logging.getLogger(__name__)


async def user_service_exception_handler(request: Request, exc: UserServiceException):
    """Handler for generic user service exceptions"""
    logger.error(f"UserServiceException: {exc.message} - Code: {exc.code}")
    response = StandardResponse.error(message=exc.message, code=exc.code)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    """Handler for user already exists exception"""
    logger.warning(f"User already exists: {exc.message}")
    response = StandardResponse.conflict(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def invalid_user_data_exception_handler(request: Request, exc: InvalidUserDataException):
    """Handler for invalid user data exception"""
    logger.warning(f"Invalid user data: {exc.message}")
    response = StandardResponse.validation_error(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    """Handler for user not found exception"""
    logger.warning(f"User not found: {exc.message}")
    response = StandardResponse.not_found(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def database_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    """Handler for database connection exception"""
    logger.error(f"Database connection error: {exc.message}")
    response = StandardResponse.internal_error(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def firebase_auth_exception_handler(request: Request, exc: FirebaseAuthException):
    """Handler for Firebase authentication exception"""
    logger.error(f"Firebase auth error: {exc.message}")
    response = StandardResponse.unauthorized(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handler for validation exception"""
    logger.warning(f"Validation error: {exc.message}")
    response = StandardResponse.validation_error(exc.message)
    return JSONResponse(status_code=int(exc.code), content=response.dict())


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for FastAPI/Pydantic validation errors"""
    logger.warning(f"Request validation error: {exc.errors()}")
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    formatted_message = "Validation errors: " + "; ".join(error_messages)
    response = StandardResponse.validation_error(formatted_message)
    return JSONResponse(status_code=422, content=response.dict())


async def general_exception_handler(request: Request, exc: Exception):
    """Handler for uncaught exceptions"""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    response = StandardResponse.internal_error("An unexpected error occurred")
    return JSONResponse(status_code=500, content=response.dict())