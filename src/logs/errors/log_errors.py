from rest_framework import status

from core.errors import AppError

class LogNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "LOG_NOT_FOUND"
    detail = "The requested logs could not be located. Please, try again."