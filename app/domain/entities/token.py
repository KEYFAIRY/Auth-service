from dataclasses import dataclass

@dataclass
class Token:
    """Domain entity representing refreshed tokens"""
    id_token: str
    refresh_token: str

    def __post_init__(self):
        if not self.id_token:
            raise ValueError("ID token is required")
        if not self.refresh_token:
            raise ValueError("Refresh token is required")

    def to_dict(self) -> dict:
        return {
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
        }