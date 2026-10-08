from rest_framework import status

from core.errors import AppError

class InvalidCEPError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_CEP"
    detail = "The provided CEP code is not a valid one. Please, try again."
    
    

class InvalidNumberError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_NUMBER"
    detail = "The provided address number is not a valid one. Please, try again."
    
    

class AddressNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "ADDRESS_NOT_FOUND"
    detail = "The requested address could not be found. Please, try again."