from app.core.exceptions import DatabaseConnectionException, UserAlreadyExistsException
from app.domain.entities.user import User
from app.infrastructure.database.mysql_connection import mysql_connection
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
from app.shared.enums import PianoLevel
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


@pytest.fixture
def user_entity():
    """Fixture que proporciona una entidad User de prueba"""
    return User(
        uid="test-uid-123",
        email="test@example.com",
        name="John Doe",
        piano_level=PianoLevel.I
    )


@pytest.fixture
def user_repository():
    """Fixture que proporciona una instancia del repositorio"""
    return MySQLUserRepository()


@pytest.fixture
def mock_session():
    """Fixture que proporciona una sesión mock"""
    session = AsyncMock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()
    session.refresh = AsyncMock()
    session.add = MagicMock()
    return session


@pytest.fixture
def mock_get_session(mock_session):
    """Fixture que proporciona el context manager mock configurado"""
    mock_cm = MagicMock()
    mock_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_cm.__aexit__ = AsyncMock(return_value=None)
    return mock_cm


class TestCreateUser:
    """Suite de pruebas para el método create_user"""

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, 
        user_repository, 
        user_entity, 
        mock_get_session,
        mock_session
    ):
        """Prueba que un usuario se crea exitosamente"""
        # Arrange
        expected_user = User(
            uid="test-uid-123",
            email="test@example.com",
            name="John Doe",
            piano_level=PianoLevel.I
        )
        
        with patch.object(mysql_connection, 'get_async_session', return_value=mock_get_session):
            user_repository._model_to_entity = MagicMock(return_value=expected_user)
            
            # Act
            result = await user_repository.create_user(user_entity)
            
            # Assert
            mock_session.add.assert_called_once()
            mock_session.commit.assert_awaited_once()
            mock_session.refresh.assert_awaited_once()
            user_repository._model_to_entity.assert_called_once()
            assert result == expected_user


    @pytest.mark.asyncio
    async def test_create_user_duplicate_uid(
        self, 
        user_repository, 
        user_entity, 
        mock_get_session,
        mock_session
    ):
        """Prueba que se lanza excepción cuando el UID ya existe"""
        # Arrange
        mock_session.commit.side_effect = IntegrityError(
            "duplicate", 
            "params", 
            "UNIQUE constraint failed: users.uid"
        )
        
        with patch.object(mysql_connection, 'get_async_session', return_value=mock_get_session):
            
            # Act & Assert
            with pytest.raises(UserAlreadyExistsException) as exc_info:
                await user_repository.create_user(user_entity)
            
            assert "UID test-uid-123" in str(exc_info.value)
            mock_session.rollback.assert_awaited_once()
            mock_session.refresh.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(
        self, 
        user_repository, 
        user_entity, 
        mock_get_session,
        mock_session
    ):
        """Prueba que se lanza excepción cuando el email ya existe"""
        # Arrange
        mock_session.commit.side_effect = IntegrityError(
            "duplicate", 
            "params", 
            "UNIQUE constraint failed: users.email"
        )
        
        with patch.object(mysql_connection, 'get_async_session', return_value=mock_get_session):
            
            # Act & Assert
            with pytest.raises(UserAlreadyExistsException) as exc_info:
                await user_repository.create_user(user_entity)
            
            assert "email test@example.com" in str(exc_info.value)
            mock_session.rollback.assert_awaited_once()


    @pytest.mark.asyncio
    async def test_create_user_generic_integrity_error(
        self, 
        user_repository, 
        user_entity, 
        mock_get_session,
        mock_session
    ):
        """Prueba manejo de IntegrityError sin información específica"""
        # Arrange
        mock_session.commit.side_effect = IntegrityError(
            "some other constraint", 
            "params", 
            "orig"
        )
        
        with patch.object(mysql_connection, 'get_async_session', return_value=mock_get_session):
            
            # Act & Assert
            with pytest.raises(UserAlreadyExistsException) as exc_info:
                await user_repository.create_user(user_entity)
            
            assert "User already exists" in str(exc_info.value)
            mock_session.rollback.assert_awaited_once()


    @pytest.mark.asyncio
    async def test_create_user_database_error(
        self, 
        user_repository, 
        user_entity, 
        mock_get_session,
        mock_session
    ):
        """Prueba manejo de errores generales de base de datos"""
        # Arrange
        db_error = SQLAlchemyError("Connection timeout")
        mock_session.commit.side_effect = db_error
        
        with patch.object(mysql_connection, 'get_async_session', return_value=mock_get_session):
            
            # Parchear el logger para evitar logs en tests
            with patch('app.infrastructure.repositories.mysql_user_repository.logger') as mock_logger:
                
                # Act & Assert
                with pytest.raises(DatabaseConnectionException):
                    await user_repository.create_user(user_entity)
                
                mock_session.rollback.assert_awaited_once()
                mock_logger.error.assert_called_once()