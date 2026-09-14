from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from rest_framework import exceptions as drf_exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler


def api_exception_handler(exc, context):
    """Normalizes Django/DB errors into DRF-shaped 4xx responses."""
    if isinstance(exc, DjangoValidationError):
        detail = exc.message_dict if hasattr(exc, "message_dict") else exc.messages
        exc = drf_exceptions.ValidationError(detail=detail)
    elif isinstance(exc, IntegrityError):
        exc = drf_exceptions.ValidationError(
            detail={"detail": "This operation violates a database constraint."}
        )

    response = exception_handler(exc, context)
    if response is None:
        return None
    return Response(response.data, status=response.status_code)
