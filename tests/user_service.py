from app.application.dto.user_dto import UpdateUserDTO
import pytest
from unittest.mock import AsyncMock, MagicMock
from app.core.exceptions import (
    UserAlreadyExistsException,
    InvalidUserDataException,
    UserNotFoundException
)
from app.domain.entities.user import User
from app.domain.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.shared.enums import PianoLevel


@pytest.fixture
def mock_user_repository():
    """Fixture que proporciona un repositorio mock"""
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repository):
    """Fixture que proporciona una instancia del servicio"""
    return UserService(mock_user_repository)


@pytest.fixture
def valid_user():
    """Fixture que proporciona un usuario válido"""
    return User(
        uid="test-uid-123",
        email="test@example.com",
        name="John Doe",
        piano_level=PianoLevel.I
    )


class TestCreateUser:
    """Suite de pruebas para crear usuario"""

    @pytest.mark.asyncio
    async def test_create_user_successfully(
        self,
        user_service,
        mock_user_repository,
        valid_user
    ):
        """
        Descripción: Crear usuario exitosamente
        Condiciones: No hay ningún usuario con el uid y correos recibidos
        Resultado esperado: Usuario correctamente guardado, se retornan uid, correo, nombre y nivel de teclado
        """
        # Arrange
        mock_user_repository.user_exists_by_uid.return_value = False
        mock_user_repository.user_exists_by_email.return_value = False
        mock_user_repository.create_user.return_value = valid_user

        # Act
        result = await user_service.create_user(valid_user)

        # Assert
        mock_user_repository.user_exists_by_uid.assert_awaited_once_with(valid_user.uid)
        mock_user_repository.user_exists_by_email.assert_awaited_once_with(valid_user.email)
        mock_user_repository.create_user.assert_awaited_once()
        
        assert result.uid == valid_user.uid
        assert result.email == valid_user.email
        assert result.name == valid_user.name
        assert result.piano_level == valid_user.piano_level


    @pytest.mark.asyncio
    async def test_create_user_with_existing_uid(
        self,
        user_service,
        mock_user_repository,
        valid_user
    ):
        """
        Descripción: Crear usuario con uid existente
        Condiciones: Existe otro usuario con mismo uid
        Resultado esperado: Excepción de usuario existente
        """
        # Arrange
        mock_user_repository.user_exists_by_uid.return_value = True

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as exc_info:
            await user_service.create_user(valid_user)

        assert f"User with UID {valid_user.uid} already exists" in str(exc_info.value)
        mock_user_repository.user_exists_by_uid.assert_awaited_once()
        mock_user_repository.create_user.assert_not_awaited()


    @pytest.mark.asyncio
    async def test_create_user_with_existing_email(
        self,
        user_service,
        mock_user_repository,
        valid_user
    ):
        """
        Descripción: Crear usuario con correo existente
        Condiciones: Existe otro usuario con mismo correo
        Resultado esperado: Excepción de usuario existente
        """
        # Arrange
        mock_user_repository.user_exists_by_uid.return_value = False
        mock_user_repository.user_exists_by_email.return_value = True

        # Act & Assert
        with pytest.raises(UserAlreadyExistsException) as exc_info:
            await user_service.create_user(valid_user)

        assert f"User with email {valid_user.email} already exists" in str(exc_info.value)
        mock_user_repository.user_exists_by_email.assert_awaited_once()
        mock_user_repository.create_user.assert_not_awaited()


class TestUpdateUser:
    """Suite de pruebas para actualizar usuario"""

    @pytest.mark.asyncio
    async def test_update_user_successfully(
        self,
        user_service,
        mock_user_repository,
        valid_user
    ):
        """
        Descripción: Actualizar usuario exitosamente
        Condiciones: Existe el usuario a actualizar y los datos son correctos
        Resultado esperado: Usuario correctamente actualizado, se retornan uid, correo, nombre y nivel de teclado
        """
        # Arrange
        update_dto = UpdateUserDTO(piano_level=PianoLevel.III)
        updated_user = User(
            uid=valid_user.uid,
            email=valid_user.email,
            name=valid_user.name,
            piano_level=PianoLevel.III
        )
        
        mock_user_repository.get_user_by_uid.return_value = valid_user
        mock_user_repository.update_user.return_value = updated_user

        # Act
        result = await user_service.update_user(valid_user.uid, update_dto)

        # Assert
        mock_user_repository.get_user_by_uid.assert_awaited_once_with(valid_user.uid)
        mock_user_repository.update_user.assert_awaited_once()
        
        assert result.uid == valid_user.uid
        assert result.piano_level == PianoLevel.III


    @pytest.mark.asyncio
    async def test_update_nonexistent_user(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: Actualizar usuario inexistente
        Condiciones: No existe el usuario a actualizar
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        uid = "nonexistent-uid"
        update_dto = UpdateUserDTO(piano_level=PianoLevel.II)
        mock_user_repository.get_user_by_uid.return_value = None

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            await user_service.update_user(uid, update_dto)

        assert f"User with UID {uid} not found" in str(exc_info.value)
        mock_user_repository.update_user.assert_not_awaited()



class TestGetUserByUid:
    """Suite de pruebas para obtener usuario por UID"""

    @pytest.mark.asyncio
    async def test_get_existing_user_by_uid(
        self,
        user_service,
        mock_user_repository,
        valid_user
    ):
        """
        Descripción: Obtener usuario existente por uid
        Condiciones: Hay un usuario registrado cuyo uid es el recibido
        Resultado esperado: Usuario correctamente retornado, con uid, correo, nombre y nivel de teclado
        """
        # Arrange
        mock_user_repository.get_user_by_uid.return_value = valid_user

        # Act
        result = await user_service.get_user_by_uid(valid_user.uid)

        # Assert
        mock_user_repository.get_user_by_uid.assert_awaited_once_with(valid_user.uid)
        assert result.uid == valid_user.uid
        assert result.email == valid_user.email
        assert result.name == valid_user.name
        assert result.piano_level == valid_user.piano_level


    @pytest.mark.asyncio
    async def test_get_nonexistent_user_by_uid(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: Obtener usuario inexistente por uid
        Condiciones: No hay ningún usuario registrado cuyo uid es el recibido
        Resultado esperado: Excepción de usuario no encontrado
        """
        # Arrange
        uid = "nonexistent-uid"
        mock_user_repository.get_user_by_uid.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundException) as exc_info:
            await user_service.get_user_by_uid(uid)

        assert f"User with UID {uid} not found" in str(exc_info.value)


class TestGetAllUsers:
    """Suite de pruebas para obtener todos los usuarios"""

    @pytest.mark.asyncio
    async def test_get_all_users_with_results(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: Obtener todos los usuarios
        Condiciones: Hay usuarios registrados
        Resultado esperado: Usuarios correctamente retornados, cada uno con uid, correo, nombre y nivel de teclado
        """
        # Arrange
        users = [
            User(uid="uid1", email="user1@example.com", name="User 1", piano_level=PianoLevel.I),
            User(uid="uid2", email="user2@example.com", name="User 2", piano_level=PianoLevel.II),
            User(uid="uid3", email="user3@example.com", name="User 3", piano_level=PianoLevel.III),
        ]
        mock_user_repository.get_all_users.return_value = users

        # Act
        result = await user_service.get_all_users()

        # Assert
        mock_user_repository.get_all_users.assert_awaited_once()
        assert len(result) == 3
        assert all(isinstance(user, User) for user in result)
        assert result[0].uid == "uid1"
        assert result[1].uid == "uid2"
        assert result[2].uid == "uid3"


    @pytest.mark.asyncio
    async def test_get_all_users_empty_list(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: Obtener todos los usuarios
        Condiciones: No hay usuarios registrados
        Resultado esperado: Lista vacía
        """
        # Arrange
        mock_user_repository.get_all_users.return_value = []

        # Act
        result = await user_service.get_all_users()

        # Assert
        mock_user_repository.get_all_users.assert_awaited_once()
        assert result == []
        assert len(result) == 0


class TestUserExists:
    """Suite de pruebas para verificar existencia de usuario"""

    @pytest.mark.asyncio
    async def test_user_exists_returns_true(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: ¿Existe un usuario con un uid dado?
        Condiciones: Hay un usuario registrado cuyo uid es el recibido
        Resultado esperado: True
        """
        # Arrange
        uid = "existing-uid"
        mock_user_repository.user_exists_by_uid.return_value = True

        # Act
        result = await user_service.user_exists(uid)

        # Assert
        mock_user_repository.user_exists_by_uid.assert_awaited_once_with(uid)
        assert result is True


    @pytest.mark.asyncio
    async def test_user_exists_returns_false(
        self,
        user_service,
        mock_user_repository
    ):
        """
        Descripción: ¿Existe un usuario con un uid dado?
        Condiciones: No hay un usuario registrado cuyo uid es el recibido
        Resultado esperado: False
        """
        # Arrange
        uid = "nonexistent-uid"
        mock_user_repository.user_exists_by_uid.return_value = False

        # Act
        result = await user_service.user_exists(uid)

        # Assert
        mock_user_repository.user_exists_by_uid.assert_awaited_once_with(uid)
        assert result is False


class TestValidateUserData:
    """Suite de pruebas para validación de datos de usuario"""

    def test_validate_user_data_with_valid_piano_level(
        self,
        user_service
    ):
        """
        Descripción: Validar datos correctos
        Condiciones: Se reciben nivel de piano válido
        Resultado esperado: No se lanza ninguna excepción
        """
        # Arrange
        valid_piano_level = PianoLevel.II

        # Act & Assert
        try:
            user_service._validate_user_data(valid_piano_level)
        except InvalidUserDataException:
            pytest.fail("No debería lanzar excepción con datos válidos")


    def test_validate_user_data_with_invalid_piano_level(
        self,
        user_service
    ):
        """
        Descripción: Validar datos incorrectos
        Condiciones: Se reciben nivel de piano inválido
        Resultado esperado: Excepción de datos de usuario inválidos
        """
        # Arrange
        invalid_piano_level = "not_a_piano_level"

        # Act & Assert
        with pytest.raises(InvalidUserDataException) as exc_info:
            user_service._validate_user_data(invalid_piano_level)

        assert "Invalid piano level" in str(exc_info.value)