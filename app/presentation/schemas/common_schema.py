from pydantic.generics import GenericModel
from typing import Optional, TypeVar, Generic
from app.shared.enums import ResponseCode

T = TypeVar("T")

class StandardResponse(GenericModel, Generic[T]):
    """Standard schema for all API responses"""
    code: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T = None, message: str = "Success", code: int = ResponseCode.SUCCESS):
        return cls(code=int(code), message=message, data=data)

    @classmethod
    def created(cls, data: T = None, message: str = "Resource created successfully"):
        return cls(code=int(ResponseCode.CREATED), message=message, data=data)

    @classmethod
    def error(cls, message: str, code: int = ResponseCode.INTERNAL_SERVER_ERROR):
        return cls(code=int(code), message=message, data=None)

    @classmethod
    def validation_error(cls, message: str = "Validation error"):
        return cls(code=int(ResponseCode.BAD_REQUEST), message=message, data=None)

    @classmethod
    def not_found(cls, message: str = "Resource not found"):
        return cls(code=int(ResponseCode.NOT_FOUND), message=message, data=None)

    @classmethod
    def conflict(cls, message: str = "Resource already exists"):
        return cls(code=int(ResponseCode.CONFLICT), message=message, data=None)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized"):
        return cls(code=int(ResponseCode.UNAUTHORIZED), message=message, data=None)

    @classmethod
    def internal_error(cls, message: str = "Internal server error"):
        return cls(code=int(ResponseCode.INTERNAL_SERVER_ERROR), message=message, data=None)
