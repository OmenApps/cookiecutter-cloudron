from django.http import HttpRequest, HttpResponse
from ninja.errors import ValidationError

from . import api


@api.exception_handler(ValidationError)
def validation_error_handler(request: HttpRequest, exc: ValidationError) -> HttpResponse:
    """Handle validation errors"""
    return api.create_response(
        request,
        {"message": "Validation error", "details": exc.errors},
        status=422,
    )


@api.exception_handler(Exception)
def generic_error_handler(request: HttpRequest, exc: Exception) -> HttpResponse:
    """Handle uncaught exceptions"""
    return api.create_response(
        request,
        {"message": "Internal server error", "details": str(exc)},
        status=500,
    )
