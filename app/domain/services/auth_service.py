from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.core.exceptions import UserAlreadyExistsException, InvalidUserDataException
from app.shared.enums import PianoLevel

class AuthDomainService:
    """Domain service for authentication business logic"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, uid: str, email: str, name: str, piano_level: PianoLevel) -> User:
        # Does user already exist ?
        if await self.user_repository.user_exists_by_uid(uid):
            raise UserAlreadyExistsException(f"User with UID {uid} already exists")

        if await self.user_repository.user_exists_by_email(email):
            raise UserAlreadyExistsException(f"User with email {email} already exists")

        # Validate user data
        self._validate_user_data(email, name, piano_level)

        # Create user entity
        user = User(
            uid=uid,
            email=email.lower().strip(),
            name=name.strip(),
            piano_level=piano_level
        )

        # Save in repository
        return await self.user_repository.create_user(user)

    def _validate_user_data(self, email: str, name: str, piano_level: PianoLevel):
        # Validate email
        if not email or len(email) < 5:
            raise InvalidUserDataException("Email must be at least 5 characters long")

        if not "@" in email or not "." in email.split("@")[1]:
            raise InvalidUserDataException("Invalid email format")

        # Validate name
        if not name or len(name.strip()) < 2:
            raise InvalidUserDataException("Name must be at least 2 characters long")

        if len(name.strip()) > 100:
            raise InvalidUserDataException("Name cannot exceed 100 characters")

        # Validate piano level
        if not isinstance(piano_level, PianoLevel):
            raise InvalidUserDataException("Invalid piano level")

    async def user_exists_by_uid(self, uid: str) -> bool:
        return await self.user_repository.user_exists_by_uid(uid)

    async def user_exists_by_email(self, email: str) -> bool:
        return await self.user_repository.user_exists_by_email(email)

    async def get_user_by_uid(self, uid: str) -> User:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise InvalidUserDataException(f"User with email {email} not found")
        return user

    async def update_user(self, user: User) -> User:
        # Does user already exist ?
        if await self.user_repository.user_exists_by_uid(user.uid):
            raise UserAlreadyExistsException(f"User with UID {user.uid} already exists")

        if await self.user_repository.user_exists_by_email(user.email):
            raise UserAlreadyExistsException(f"User with email {user.email} already exists")

        self._validate_user_data(user.email, user.name, user.piano_level)
        
        return await self.user_repository.update_user(user)

    async def delete_user(self, uid: str) -> bool:
        user = await self.user_repository.get_user_by_uid(uid)
        if not user:
            raise InvalidUserDataException(f"User with UID {uid} not found")
        return await self.user_repository.delete_user(uid)