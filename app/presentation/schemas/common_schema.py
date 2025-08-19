from pydantic import BaseModel
from typing import Optional, Any
from app.shared.enums import ResponseCode


class StandardResponse(BaseModel):
    """Standard schema for all API responses"""
    code: str
    message: str
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Any = None, message: str = "Success", code: str = ResponseCode.SUCCESS):
        """Create a successful response"""
        return cls(code=code, message=message, data=data)

    @classmethod
    def created(cls, data: Any = None, message: str = "Resource created successfully"):
        """Create a resource created response"""
        return cls(code=ResponseCode.CREATED, message=message, data=data)

    @classmethod
    def error(cls, message: str, code: str = ResponseCode.INTERNAL_SERVER_ERROR):
        """Create an error response"""
        return cls(code=code, message=message, data=None)

    @classmethod
    def validation_error(cls, message: str = "Validation error"):
        """Create a validation error response"""
        return cls(code=ResponseCode.BAD_REQUEST, message=message, data=None)

    @classmethod
    def not_found(cls, message: str = "Resource not found"):
        """Create a not found response"""
        return cls(code=ResponseCode.NOT_FOUND, message=message, data=None)

    @classmethod
    def conflict(cls, message: str = "Resource already exists"):
        """Create a conflict response"""
        return cls(code=ResponseCode.CONFLICT, message=message, data=None)

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized"):
        """Create an unauthorized response"""
        return cls(code=ResponseCode.UNAUTHORIZED, message=message, data=None)

    @classmethod
    def internal_error(cls, message: str = "Internal server error"):
        """Create an internal error response"""
        return cls(code=ResponseCode.INTERNAL_SERVER_ERROR, message=message, data=None)