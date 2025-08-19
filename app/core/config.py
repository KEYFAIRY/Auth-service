import os
from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import Field

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    APP_NAME: str = "Auth Service"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "qa")
    DEBUG: bool = ENVIRONMENT == "qa"
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = Field(default=8000, alias="AUTH_SERVICE_PORT")
    RELOAD: bool = DEBUG
    
    # Configuración de base de datos MySQL
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB: str = os.getenv("MYSQL_DB", "auth_db")
    
    # URLs de conexión a base de datos
    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )
    
    # Configuración de Firebase
    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH", 
        "./firebase_account.json"
    )
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO" if not DEBUG else "DEBUG"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de Rate Limiting
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de configuración
settings = Settings()
