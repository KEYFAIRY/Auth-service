from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.core.exceptions import (
    AuthServiceException,
    UserAlreadyExistsException,
    InvalidUserDataException,
    UserNotFoundException,
    DatabaseConnectionException,
    FirebaseAuthException,
    ValidationException
)
from app.presentation.schemas.common_schema import StandardResponse
from app.shared.enums import ResponseCode
import logging

logger = logging.getLogger(__name__)


async def auth_service_exception_handler(request: Request, exc: AuthServiceException):
    """Manejador para excepciones del servicio de autenticación"""
    logger.error(f"AuthServiceException: {exc.message} - Code: {exc.code}")
    
    response = StandardResponse.error(
        message=exc.message,
        code=exc.code
    )
    
    # Mapear código de excepción a código HTTP
    status_code = _get_http_status_code(exc.code)
    
    return JSONResponse(
        status_code=status_code,
        content=response.dict()
    )


async def user_already_exists_exception_handler(request: Request, exc: UserAlreadyExistsException):
    """Manejador para excepción de usuario ya existente"""
    logger.warning(f"User already exists: {exc.message}")
    
    response = StandardResponse.conflict(exc.message)
    
    return JSONResponse(
        status_code=409,
        content=response.dict()
    )


async def invalid_user_data_exception_handler(request: Request, exc: InvalidUserDataException):
    """Manejador para datos de usuario inválidos"""
    logger.warning(f"Invalid user data: {exc.message}")
    
    response = StandardResponse.validation_error(exc.message)
    
    return JSONResponse(
        status_code=422,
        content=response.dict()
    )


async def user_not_found_exception_handler(request: Request, exc: UserNotFoundException):
    """Manejador para usuario no encontrado"""
    logger.warning(f"User not found: {exc.message}")
    
    response = StandardResponse.not_found(exc.message)
    
    return JSONResponse(
        status_code=404,
        content=response.dict()
    )


async def database_connection_exception_handler(request: Request, exc: DatabaseConnectionException):
    """Manejador para errores de conexión a base de datos"""
    logger.error(f"Database connection error: {exc.message}")
    
    response = StandardResponse.internal_error("Database connection error")
    
    return JSONResponse(
        status_code=500,
        content=response.dict()
    )


async def firebase_auth_exception_handler(request: Request, exc: FirebaseAuthException):
    """Manejador para errores de autenticación con Firebase"""
    logger.error(f"Firebase auth error: {exc.message}")
    
    response = StandardResponse.unauthorized(exc.message)
    
    return JSONResponse(
        status_code=401,
        content=response.dict()
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Manejador para errores de validación"""
    logger.warning(f"Validation error: {exc.message}")
    
    response = StandardResponse.validation_error(exc.message)
    
    return JSONResponse(
        status_code=400,
        content=response.dict()
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador para errores de validación de FastAPI/Pydantic"""
    logger.warning(f"Request validation error: {exc.errors()}")
    
    # Formatear errores de validación
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    formatted_message = "Validation errors: " + "; ".join(error_messages)
    
    response = StandardResponse.validation_error(formatted_message)
    
    return JSONResponse(
        status_code=422,
        content=response.dict()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Manejador para excepciones generales no capturadas"""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    
    response = StandardResponse.internal_error("An unexpected error occurred")
    
    return JSONResponse(
        status_code=500,
        content=response.dict()
    )


def _get_http_status_code(error_code: str) -> int:
    """Mapear código de error a código HTTP"""
    code_mapping = {
        ResponseCode.SUCCESS: 200,
        ResponseCode.CREATED: 201,
        ResponseCode.ACCEPTED: 202,
        ResponseCode.BAD_REQUEST: 400,
        ResponseCode.UNAUTHORIZED: 401,
        ResponseCode.FORBIDDEN: 403,
        ResponseCode.NOT_FOUND: 404,
        ResponseCode.CONFLICT: 409,
        ResponseCode.UNPROCESSABLE_ENTITY: 422,
        ResponseCode.INTERNAL_SERVER_ERROR: 500,
        ResponseCode.SERVICE_UNAVAILABLE: 503,
    }
    
    return code_mapping.get(error_code, 500)