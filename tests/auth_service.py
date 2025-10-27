from app.domain.entities.auth import Auth
from app.domain.entities.login import Login
from app.domain.entities.token import Token
import pytest
from unittest.mock import AsyncMock
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidUserDataException,
    UserNotFoundException,
    FirebaseAuthException
)
from app.domain.services.auth_service import AuthService
from app.domain.repositories.auth_repository import AuthRepository


@pytest.fixture
def mock_auth_repository():
    """Fixture que proporciona un repositorio mock"""
    return AsyncMock(spec=AuthRepository)


@pytest.fixture
def auth_service(mock_auth_repository):
    """Fixture que proporciona una instancia del servicio"""
    return AuthService(mock_auth_repository)


@pytest.fixture
def valid_auth():
    """Fixture que proporciona una entidad Auth válida"""
    return Auth(
        uid="test-uid-123",
        email="test@example.com"
    )


@pytest.fixture
def valid_login():
    """Fixture que proporciona una entidad Login válida"""
    return Login(
        uid="test-uid-123",
        email="test@example.com",
        id_token="test-id-token",
        refresh_token="test-refresh-token"
    )


@pytest.fixture
def valid_token():
    """Fixture que proporciona una entidad Token válida"""
    return Token(
        id_token="new-id-token",
        refresh_token="new-refresh-token"
    )


class TestRegisterUser:
    """Suite de pruebas para registrar usuario"""

    @pytest.mark.asyncio
    async def test_register_user_successfully(
        self,
        auth_service,
        mock_auth_repository,
        valid_auth
    ):
        """
        Descripción: Registrar credenciales de usuario exitosamente
        Condiciones: El correo no ha sido previamente utilizado por otro usuario
        Resultado esperado: Credenciales correctamente registradas y se retornan correo y uid del nuevo usuario
        """
        # Arrange
        email = "newuser@example.com"
        password = "password123"
        mock_auth_repository.register_user.return_value = valid_auth

        # Act
        result = await auth_service.register_user(email, password)

        # Assert
        mock_auth_repository.register_user.assert_awaited_once_with(email, password)
        assert result.uid == valid_auth.uid
        assert result.email == valid_auth.email


    @pytest.mark.asyncio
    async def test_register_user_with_existing_email(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Registrar credenciales de usuario con correo existente
        Condiciones: El correo ha sido previamente utilizado por otro usuario
        Resultado esperado: Excepción de usuario existente
        """
        # Arrange
        email = "existing@example.com"
        password = "password123"
        mock_auth_repository.register_user.side_effect = UserAlreadyExistsException(
            f"User with email {email} already exists"
        )

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException):
            await auth_service.register_user(email, password)

        mock_auth_repository.register_user.assert_awaited_once_with(email, password)


    @pytest.mark.asyncio
    async def test_register_user_with_invalid_email(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Registrar usuario con email inválido
        Condiciones: El email no tiene formato válido
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        invalid_email = "notanemail"
        password = "password123"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.register_user(invalid_email, password)

        assert "Invalid email format" in str(exc_info.value)
        mock_auth_repository.register_user.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_register_user_with_short_password(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Registrar usuario con contraseña corta
        Condiciones: La contraseña tiene menos de 6 caracteres
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        email = "user@example.com"
        short_password = "12345"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.register_user(email, short_password)

        assert "Password must be at least 6 characters long" in str(exc_info.value)
        mock_auth_repository.register_user.assert_not_awaited()


class TestLogin:
    """Suite de pruebas para iniciar sesión"""

    @pytest.mark.asyncio
    async def test_login_with_correct_credentials(
        self,
        auth_service,
        mock_auth_repository,
        valid_login
    ):
        """
        Descripción: Iniciar sesión con credenciales correctas
        Condiciones: Las credenciales están registradas y son correctas
        Resultado esperado: Inicio de sesión exitoso y se retorna uid, correo, id token y refresh token
        """
        # Arrange
        email = "user@example.com"
        password = "password123"
        mock_auth_repository.login.return_value = valid_login

        # Act
        result = await auth_service.login(email, password)

        # Assert
        mock_auth_repository.login.assert_awaited_once_with(email, password)
        assert result.uid == valid_login.uid
        assert result.email == valid_login.email
        assert result.id_token == valid_login.id_token
        assert result.refresh_token == valid_login.refresh_token


    @pytest.mark.asyncio
    async def test_login_with_incorrect_credentials(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Iniciar sesión con credenciales incorrectas
        Condiciones: Las credenciales son incorrectas o no han sido registradas
        Resultado esperado: Excepción de usuario no encontrado
        """
        # Arrange
        email = "user@example.com"
        password = "wrongpassword"
        mock_auth_repository.login.return_value = None

        # Act & Assert
        with pytest.raises(FirebaseAuthException) as exc_info:
            await auth_service.login(email, password)

        assert "User not found or invalid credentials" in str(exc_info.value)
        mock_auth_repository.login.assert_awaited_once_with(email, password)



    @pytest.mark.asyncio
    async def test_login_with_invalid_email(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Iniciar sesión con email inválido
        Condiciones: El email no tiene formato válido
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        invalid_email = "notanemail"
        password = "password123"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.login(invalid_email, password)

        assert "Invalid email format" in str(exc_info.value)
        mock_auth_repository.login.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_login_with_short_password(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Iniciar sesión con contraseña corta
        Condiciones: La contraseña tiene menos de 6 caracteres
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        email = "user@example.com"
        short_password = "12345"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.login(email, short_password)

        assert "Password must be at least 6 characters long" in str(exc_info.value)
        mock_auth_repository.login.assert_not_awaited()


class TestRefreshToken:
    """Suite de pruebas para renovar token"""

    @pytest.mark.asyncio
    async def test_refresh_token_successfully(
        self,
        auth_service,
        mock_auth_repository,
        valid_token
    ):
        """
        Descripción: Renovar token exitosamente
        Condiciones: El refresh token es correcto
        Resultado esperado: Token renovado correctamente y se retorna id token y refresh token
        """
        # Arrange
        refresh_token = "valid-refresh-token"
        mock_auth_repository.refresh_token.return_value = valid_token

        # Act
        result = await auth_service.refresh_token(refresh_token)

        # Assert
        mock_auth_repository.refresh_token.assert_awaited_once_with(refresh_token)
        assert result.id_token == valid_token.id_token
        assert result.refresh_token == valid_token.refresh_token


    @pytest.mark.asyncio
    async def test_refresh_token_with_empty_token(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Renovar token con refresh token vacío
        Condiciones: El refresh token no fue enviado a la solicitud o su longitud es cero
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        empty_token = ""

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.refresh_token(empty_token)

        assert "Refresh token is required" in str(exc_info.value)
        mock_auth_repository.refresh_token.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_refresh_token_with_none_token(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Renovar token con refresh token None
        Condiciones: El refresh token es None
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        none_token = None

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.refresh_token(none_token)

        assert "Refresh token is required" in str(exc_info.value)
        mock_auth_repository.refresh_token.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_refresh_token_with_whitespace_only(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Renovar token con refresh token solo espacios
        Condiciones: El refresh token contiene solo espacios en blanco
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        whitespace_token = "   "

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await auth_service.refresh_token(whitespace_token)

        assert "Refresh token is required" in str(exc_info.value)
        mock_auth_repository.refresh_token.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_refresh_token_with_invalid_token(
        self,
        auth_service,
        mock_auth_repository
    ):
        """
        Descripción: Renovar token con refresh token inválido
        Condiciones: El token no es correcto o no fue emitido por Firebase
        Resultado esperado: Excepción de autenticación de Firebase
        """
        # Arrange
        invalid_token = "invalid-token"
        mock_auth_repository.refresh_token.side_effect = Exception("Invalid refresh token")

        # Act & Assert
        with pytest.raises(FirebaseAuthException) as exc_info:
            await auth_service.refresh_token(invalid_token)

        assert "Invalid refresh token" in str(exc_info.value)
        mock_auth_repository.refresh_token.assert_awaited_once_with(invalid_token)


class TestValidateCredentials:
    """Suite de pruebas para validación de credenciales"""

    def test_validate_credentials_with_valid_data(
        self,
        auth_service
    ):
        """
        Descripción: Validar credenciales correctas
        Condiciones: Email y password son válidos
        Resultado esperado: No se lanza ninguna excepción
        """
        # Arrange
        email = "user@example.com"
        password = "password123"

        # Act & Assert
        try:
            auth_service._validate_credentials(email, password)
        except InvalidUserDataException:
            pytest.fail("No debería lanzar excepción con datos válidos")


    def test_validate_credentials_with_empty_email(
        self,
        auth_service
    ):
        """
        Descripción: Validar credenciales con email vacío
        Condiciones: El email está vacío
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        email = ""
        password = "password123"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            auth_service._validate_credentials(email, password)

        assert "Invalid email format" in str(exc_info.value)


    def test_validate_credentials_with_email_without_at(
        self,
        auth_service
    ):
        """
        Descripción: Validar credenciales con email sin @
        Condiciones: El email no contiene el símbolo @
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        email = "notanemail.com"
        password = "password123"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            auth_service._validate_credentials(email, password)

        assert "Invalid email format" in str(exc_info.value)


    def test_validate_credentials_with_empty_password(
        self,
        auth_service
    ):
        """
        Descripción: Validar credenciales con password vacío
        Condiciones: El password está vacío
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        email = "user@example.com"
        password = ""

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            auth_service._validate_credentials(email, password)

        assert "Password must be at least 6 characters long" in str(exc_info.value)