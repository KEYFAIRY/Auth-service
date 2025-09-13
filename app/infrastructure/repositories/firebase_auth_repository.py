import aiohttp
import firebase_admin.auth as firebase_auth
from app.domain.repositories.auth_repository import AuthRepository
from app.domain.entities.auth import Auth
from app.domain.entities.login import Login
from app.domain.entities.token import Token
from app.core.exceptions import (
    UserAlreadyExistsException,
    FirebaseAuthException,
    UserNotFoundException,
)
from app.core.firebase_config import get_web_api_key


class FirebaseAuthRepository(AuthRepository):
    """Auth repository implementation using Firebase Authentication"""

    async def register_user(self, email: str, password: str) -> Auth:
        try:
            user = firebase_auth.create_user(email=email, password=password)
            return Auth(uid=user.uid, email=user.email)
        except firebase_auth.EmailAlreadyExistsError:
            raise UserAlreadyExistsException()
        except Exception as e:
            raise FirebaseAuthException(str(e))

    async def login(self, email: str, password: str) -> Login:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={get_web_api_key()}"
        payload = {"email": email, "password": password, "returnSecureToken": True}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    raise UserNotFoundException("Invalid credentials")
                data = await resp.json()
                return Login(
                    uid=data["localId"],
                    email=data["email"],
                    id_token=data["idToken"],
                    refresh_token=data["refreshToken"],
                )

    async def refresh_token(self, refresh_token: str) -> Token:
        url = f"https://securetoken.googleapis.com/v1/token?key={get_web_api_key()}"
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload) as resp:
                if resp.status != 200:
                    raise FirebaseAuthException("Invalid refresh token")
                data = await resp.json()
                return Token(
                    id_token=data["id_token"],
                    refresh_token=data["refresh_token"],
                )