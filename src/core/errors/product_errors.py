from rest_framework import status

from core.errors import AppError

class InvalidValueError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_VALUE"
    detail = "The provided value for this resource is invalid. Please, try again."



class ProductNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "PRODUCT_NOT_fOUND"
    detail = "The requested product could not be found. Please, try again."