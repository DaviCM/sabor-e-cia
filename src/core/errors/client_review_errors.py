from rest_framework import status

from core.errors import AppError

class ClientReviewNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "CLIENT_REVIEW_NOT_FOUND"
    detail = "The requested client review could not be found. Please, try again."



class InvalidScoreError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_SCORE"
    detail = "The review score must be between 1 and 5. Please, try again."



class InvalidReviewDateError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_REVIEW_DATE"
    detail = "The provided date range for client reviews is invalid. Please, try again."
