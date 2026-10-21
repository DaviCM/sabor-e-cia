from rest_framework import status

from core.errors import AppError

class InvalidTotalValueError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_TOTAL_VALUE"
    detail = "The total value for this order is invalid. Please, try again."



class InvalidQuantitiesError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_QUANTITIES"
    detail = "The quantity for one or more products within this order is invalid. Please, try again."



class OrderNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "ORDER_NOT_FOUND"
    detail = "The requested order could not be found. Please, try again."

