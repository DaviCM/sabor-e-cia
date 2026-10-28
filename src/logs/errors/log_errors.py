from rest_framework import status

from core.errors import AppError

class LogNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "LOG_NOT_FOUND"
    detail = "The requested logs could not be located. Please, try again."



class InvalidLogDateError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_LOG_DATE"
    detail = "The provided date range for logs is invalid. Please, try again."



class InvalidPaymentMethodError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_PAYMENT_METHOD"
    detail = "The provided payment method is invalid. Please, try again."
