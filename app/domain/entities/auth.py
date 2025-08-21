from dataclasses import dataclass

@dataclass
class Auth:
    """Domain entity representing a registered user (after creation)"""
    uid: str
    email: str

    def __post_init__(self):
        if not self.uid:
            raise ValueError("UID is required")
        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "email": self.email,
        }
