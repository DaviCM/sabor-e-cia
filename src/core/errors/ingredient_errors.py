from rest_framework import status

from core.errors import AppError

class InvalidQuantityError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_QUANTITY"
    detail = "The provided quantity for this ingredient is invalid. Please, try again."



class IngredientNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "INGREDIENT_NOT_FOUND"
    detail = "The requested ingredient could not be found. Please, try again."