from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import sys

# Imports locales
from app.core.config import settings
from app.core.exceptions import (
    UserServiceException,
    UserAlreadyExistsException,
    InvalidUserDataException,
    UserNotFoundException,
    DatabaseConnectionException,
    FirebaseAuthException,
    ValidationException
)
from app.presentation.api.v1.users import router as users_router
from app.presentation.api.v1.auth import router as auth_router
from app.presentation.middleware.exception_handler import (
    user_service_exception_handler,
    user_already_exists_exception_handler,
    invalid_user_data_exception_handler,
    user_not_found_exception_handler,
    database_connection_exception_handler,
    firebase_auth_exception_handler,
    validation_exception_handler,
    request_validation_exception_handler,
    general_exception_handler
)
from app.infrastructure.database.mysql_connection import db_connection


# Configure application logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log") if settings.ENVIRONMENT != "development" else logging.NullHandler()
    ]
)

# Reduce FastAPI/Uvicorn log verbosity
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("fastapi").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    try:
        # Inicializar conexión a base de datos
        logger.info("Initializing database connection...")
        db_connection.create_async_engine()
        
    except Exception as e:
        logger.error(f"Error initializing application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    try:
        await db_connection.close_connections()
        logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")


def create_application() -> FastAPI:
    """Crear y configurar la aplicación FastAPI"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Microservicio de autenticación con Firebase y gestión de usuarios",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar manejadores de excepciones
    app.add_exception_handler(UserServiceException, user_service_exception_handler)
    app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler)
    app.add_exception_handler(InvalidUserDataException, invalid_user_data_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, database_connection_exception_handler)
    app.add_exception_handler(FirebaseAuthException, firebase_auth_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    # Registrar rutas
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")

    # Endpoint de health check
    @app.get("/health")
    async def health_check():
        """Endpoint para verificar el estado de la aplicación"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        }
    
    @app.get("/")
    async def root():
        """Endpoint raíz"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs_url": "/docs" if settings.DEBUG else "Documentation not available in production"
        }
    
    return app


# Crear instancia de la aplicación
app = create_application()


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower()
    )
