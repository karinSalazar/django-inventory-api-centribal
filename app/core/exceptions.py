from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def global_exception_handler(exc, context):
    """Manejador global para que la API siempre responda con un JSON coherente."""
    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {"error": "Internal Server Error", "detail": str(exc)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    return response