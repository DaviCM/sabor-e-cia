from rest_framework import status

from core.errors import AppError

class InvalidMultiplierError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_MULTIPLIER"
    detail = "The provided multiplier cannot be used in a coupom. Please, try again."



class InvalidDateError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_DATE"
    detail = "The provided expiration date is lower than the creation date. Please, try again"



class CoupomNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "COUPOM_NOT_FOUND"
    detail = "The requested coupom could not be found. Please, try again."