from dataclasses import dataclass

@dataclass
class Login:
    """Domain entity representing a successful login"""
    uid: str
    email: str
    id_token: str
    refresh_token: str

    def __post_init__(self):
        if not self.uid:
            raise ValueError("UID is required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")
        if not self.id_token:
            raise ValueError("ID token is required")
        if not self.refresh_token:
            raise ValueError("Refresh token is required")

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "email": self.email,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
        }
