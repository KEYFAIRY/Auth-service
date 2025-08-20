from app.core.exceptions import InvalidUserDataException
from app.shared.enums import PianoLevel

# Convert string to enum, raises ValueError if invalid
def parse_piano_level(level_str: str) -> str:
    try:
        return PianoLevel(level_str).value
    except ValueError:
        raise InvalidUserDataException("Valid piano level is required")
