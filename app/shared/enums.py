from enum import Enum

class PianoLevel(str, Enum):
    I = "teclado I"
    II = "teclado II"
    III = "teclado III"
    IV = "teclado IV"

class ResponseCode(int, Enum):
    # 2xx Success codes
    SUCCESS = 200
    CREATED = 201
    ACCEPTED = 202
    
    # 4xx Client error codes
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    
    # 5xx Server error codes
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503