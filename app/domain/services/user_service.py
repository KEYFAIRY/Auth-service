from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.core.exceptions import UserAlreadyExistsException, InvalidUserDataException
from app.shared.enums import PianoLevel
from app.application.dto.user_dto import CreateUserDTO, UpdateUserDTO


class UserService:
    """Domain service for user business logic"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, dto: CreateUserDTO) -> User:
        # Check existence
        if await self.user_repository.user_exists_by_uid(dto.uid):
            raise UserAlreadyExistsException(f"User with UID {dto.uid} already exists")
        if await self.user_repository.user_exists_by_email(dto.email):
            raise UserAlreadyExistsException(f"User with email {dto.email} already exists")

        self._validate_user_data(dto.email, dto.name, dto.piano_level)

        user = User(
            uid=dto.uid,
            email=dto.email.lower().strip(),
            name=dto.name.strip(),
            piano_level=dto.piano_level
        )

        return await self.user_repository.create_user(user)

    async def update_user(self, uid: str, dto: UpdateUserDTO) -> User:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")

        # Update fields
        user.name = dto.name or user.name
        user.email = dto.email or user.email
        user.piano_level = dto.piano_level or user.piano_level

        self._validate_user_data(user.email, user.name, user.piano_level)

        return await self.user_repository.update_user(user)

    async def get_user_by_uid(self, uid: str) -> User:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")
        return user

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def delete_user(self, uid: str) -> bool:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")
        return await self.user_repository.delete_user(uid)

    async def user_exists(self, uid: str) -> bool:
        return await self.user_repository.user_exists_by_uid(uid)

    def _validate_user_data(self, email: str, name: str, piano_level: PianoLevel):
        if not email or len(email) < 5 or "@" not in email or "." not in email.split("@")[1]:
            raise InvalidUserDataException("Invalid email format")
        if not name or len(name.strip()) < 2 or len(name.strip()) > 100:
            raise InvalidUserDataException("Invalid name length")
        if not isinstance(piano_level, PianoLevel):
            raise InvalidUserDataException("Invalid piano level")
