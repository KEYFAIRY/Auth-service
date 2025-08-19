from typing import Optional


class AuthServiceException(Exception):
    """Base exception for the authentication service"""
    def __init__(self, message: str, code: str = "500"):
        self.message = message
        self.code = code
        super().__init__(message)


class UserAlreadyExistsException(AuthServiceException):
    """User already exists in the system"""
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, "409")


class InvalidUserDataException(AuthServiceException):
    """Invalid user data"""
    def __init__(self, message: str = "Invalid user data"):
        super().__init__(message, "422")


class UserNotFoundException(AuthServiceException):
    """User not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, "404")


class DatabaseConnectionException(AuthServiceException):
    """Database connection error"""
    def __init__(self, message: str = "Database connection error"):
        super().__init__(message, "500")


class FirebaseAuthException(AuthServiceException):
    """Firebase authentication error"""
    def __init__(self, message: str = "Firebase authentication error"):
        super().__init__(message, "401")


class ValidationException(AuthServiceException):
    """Data validation error"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, "400")