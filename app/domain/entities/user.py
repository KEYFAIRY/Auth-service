from dataclasses import dataclass
from app.shared.enums import PianoLevel


@dataclass
class User:
    """Domain entity for the user"""
    uid: str
    email: str
    name: str
    piano_level: PianoLevel

    def __post_init__(self):
        """Entity validations"""
        if not self.uid:
            raise ValueError("UID is required")

        if not self.email or "@" not in self.email:
            raise ValueError("Valid email is required")

        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Name is required")

        if not isinstance(self.piano_level, PianoLevel):
            raise ValueError("Valid piano level is required")

    def to_dict(self) -> dict:
        """Converts the entity to a dictionary"""
        return {
            "uid": self.uid,
            "email": self.email,
            "name": self.name,
            "piano_level": self.piano_level.value,
        }