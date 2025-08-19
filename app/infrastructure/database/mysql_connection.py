import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.exceptions import DatabaseConnectionException
from app.infrastructure.database.models.user_model import Base
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manejo de conexión a MySQL"""
    
    def __init__(self):
        self.mysql_host = os.getenv("MYSQL_HOST", "localhost")
        self.mysql_port = os.getenv("MYSQL_PORT", "3306")
        self.mysql_user = os.getenv("MYSQL_USER", "root")
        self.mysql_password = os.getenv("MYSQL_PASSWORD", "")
        self.mysql_db = os.getenv("MYSQL_DB", "auth_db")
        
        # URL de conexión asíncrona
        self.async_database_url = (
            f"mysql+aiomysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}"
        )

        
        self.async_engine = None
        self.async_session_factory = None
    
    def create_async_engine(self):
        """Crear motor asíncrono de base de datos"""
        try:
            self.async_engine = create_async_engine(
                self.async_database_url,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.async_session_factory = async_sessionmaker(
                self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            logger.info("Async database engine created successfully")
        except Exception as e:
            logger.error(f"Error creating async database engine: {e}")
            raise DatabaseConnectionException(f"Failed to create database connection: {str(e)}")
    

    def get_async_session(self) -> AsyncSession:
        """Obtener sesión asíncrona"""
        if not self.async_session_factory:
            self.create_async_engine()
        
        return self.async_session_factory()
    
    async def close_connections(self):
        """Cerrar conexiones a la base de datos"""
        if self.async_engine:
            await self.async_engine.dispose()
            logger.info("Database connections closed")


# Instancia global de conexión
db_connection = DatabaseConnection()
