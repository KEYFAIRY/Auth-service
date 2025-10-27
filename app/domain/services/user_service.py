from app.application.dto.user_dto import UpdateUserDTO
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.core.exceptions import UserAlreadyExistsException, InvalidUserDataException, UserNotFoundException
from app.shared.enums import PianoLevel

class UserService:
    """Domain service for user business logic"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user: User) -> User:
        # Check existence
        if await self.user_repository.user_exists_by_uid(user.uid):
            raise UserAlreadyExistsException(f"User with UID {user.uid} already exists")
        if await self.user_repository.user_exists_by_email(user.email):
            raise UserAlreadyExistsException(f"User with email {user.email} already exists")

        self._validate_user_data(user.piano_level)

        user = User(
            uid=user.uid,
            email=user.email.lower().strip(),
            name=user.name.strip(),
            piano_level=user.piano_level
        )

        return await self.user_repository.create_user(user)

    async def update_user(self, uid: str, updated_user: UpdateUserDTO) -> User:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")
        
        # Update fields
        user.piano_level = updated_user.piano_level or user.piano_level

        self._validate_user_data(user.piano_level)

        return await self.user_repository.update_user(user)

    async def get_user_by_uid(self, uid: str) -> User:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise UserNotFoundException(f"User with UID {uid} not found")
        return user

    async def get_all_users(self) -> list[User]:
        return await self.user_repository.get_all_users()

    async def user_exists(self, uid: str) -> bool:
        return await self.user_repository.user_exists_by_uid(uid)

    def _validate_user_data(self, piano_level: PianoLevel):
        if not isinstance(piano_level, PianoLevel):
            raise InvalidUserDataException("Invalid piano level")
