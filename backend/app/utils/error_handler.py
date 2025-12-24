"""
Error handling utilities for consistent error responses.

This module provides standardized error handling and response formatting
across the application to ensure consistent API error responses.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception class for application-specific errors."""
    
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppException):
    """Exception for resource not found errors."""
    
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource} not found"
        if identifier:
            message += f": {identifier}"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppException):
    """Exception for unauthorized access errors."""
    
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    """Exception for forbidden access errors."""
    
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)


class ValidationAppError(AppException):
    """Exception for validation errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, details=details)


class ConflictError(AppException):
    """Exception for resource conflict errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT, details=details)


def create_error_response(
    message: str,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    details: dict = None,
    error_code: str = None
) -> JSONResponse:
    """
    Create a standardized error response.

    Args:
        message: Error message
        status_code: HTTP status code
        details: Additional error details
        error_code: Optional error code for client-side handling

    Returns:
        JSONResponse with standardized error format
    """
    error_response = {
        "error": {
            "message": message,
            "status_code": status_code
        }
    }

    if error_code:
        error_response["error"]["code"] = error_code

    if details:
        error_response["error"]["details"] = details

    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handler for application-specific exceptions.

    Args:
        request: FastAPI request object
        exc: Application exception

    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Application error: {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
            "details": exc.details
        }
    )

    return create_error_response(
        message=exc.message,
        status_code=exc.status_code,
        details=exc.details
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handler for request validation errors.

    Args:
        request: FastAPI request object
        exc: Validation exception

    Returns:
        JSONResponse with validation error details
    """
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(
        f"Validation error: {errors}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "errors": errors
        }
    )

    return create_error_response(
        message="Validation error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        details={"validation_errors": errors},
        error_code="VALIDATION_ERROR"
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler for unhandled exceptions.

    Args:
        request: FastAPI request object
        exc: Exception

    Returns:
        JSONResponse with generic error message
    """
    logger.exception(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": type(exc).__name__
        }
    )

    return create_error_response(
        message="An internal server error occurred",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="INTERNAL_SERVER_ERROR"
    )

