from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import logging
import sys
import asyncio

# Local imports
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
from app.core.logging import configure_logging
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
from app.infrastructure.database import mysql_connection


# Configure logging 
configure_logging()
logger = logging.getLogger(__name__)


async def initialize_databases(retry_delay: int = 5):
    mysql_connected = False
    attempt = 0
    
    while not (mysql_connected):
        logger.info(f"Reintentando conexión a BDs (intento {attempt + 1})...")
        await asyncio.sleep(retry_delay)
        
        attempt += 1
        
        # MySQL
        if not mysql_connected:
            try:
                mysql_connection.mysql_connection.init_engine()
                await mysql_connection.mysql_connection.verify_connection()
                mysql_connected = True
            except Exception as e:
                logger.warning(f"⚠️  MySQL connection failed: {e}")
    
    logger.info("✅ Todas las conexiones de BD establecidas y verificadas")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # ---------- DB Connections ----------
    await initialize_databases(retry_delay=5)
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    # Close DBs
    await mysql_connection.mysql_connection.close_connections()


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
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register exception handlers
    app.add_exception_handler(UserServiceException, user_service_exception_handler)
    app.add_exception_handler(UserAlreadyExistsException, user_already_exists_exception_handler)
    app.add_exception_handler(InvalidUserDataException, invalid_user_data_exception_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_exception_handler)
    app.add_exception_handler(DatabaseConnectionException, database_connection_exception_handler)
    app.add_exception_handler(FirebaseAuthException, firebase_auth_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    # Register routes
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")

    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT
        }
    
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs_url": "/docs" if settings.DEBUG else "Documentation not available in production"
        }
    
    return app


# Create the FastAPI application instance
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
