from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Configuración de la aplicación
    APP_NAME: str = "Auth Service"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="qa")
    DEBUG: bool = Field(default=False)

    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = Field(default=8000, alias="AUTH_SERVICE_PORT")
    RELOAD: bool = False

    # Configuración de base de datos MySQL
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str

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
    FIREBASE_CREDENTIALS_PATH: str = Field(..., description="Path al archivo de credenciales Firebase")
    FIREBASE_WEB_API_KEY: str = Field(..., description="Firebase Web API Key")

    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configuración de CORS (luego)
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]


    # Configuración de Rate Limiting (luego)
    RATE_LIMIT_CALLS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"

    def configure(self):
        self.DEBUG = self.ENVIRONMENT == "qa"
        self.RELOAD = self.DEBUG
        self.LOG_LEVEL = "DEBUG" if self.DEBUG else "INFO"


# Instancia global de configuración
settings = Settings()
settings.configure()
