from rest_framework import status

from core.errors import AppError

class InvalidEmailError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_EMAIL"
    detail = "The provided e-mail address cannot be used to create an user. Please, try again."
    
    

class InvalidPhoneError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_PHONE"
    detail = "The provided phone number cannot be used to create an user. Please, try again."
   
    

class InvalidCPFError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_CPF"
    detail = "The provided CPF code cannot be used to create an user. Please, try again."



class InvalidRoleError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    error = "INVALID_ROLE"
    detail = "The provided role for this user cannot be accepted. Please, try again."
    
    

class UserAlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    error = "USER_ALREADY_EXISTS"
    detail = "An user with the provided information is already signed up. Please, sign in or try again."
    
    
    
class PhoneAlreadyExistsError(AppError):
    status_code = status.HTTP_409_CONFLICT
    error = "PHONE_ALREADY_EXISTS"
    detail = "The provided phone number is already registered in the system. Please, try again."
    
    

class EmployeeNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "EMPLOYEE_NOT_FOUND"
    detail = "The requested employee could not be retrieved or signed in. Please, try again."



class ClientNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "CLIENT_NOT_FOUND"
    detail = "The requested client could not be retrieved or signed in. Please, try again."



class UserNotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    error = "USER_NOT_FOUND"
    detail = "The requested user could not be retrieved or signed in. Please, try again."



class UserHasNoPermissionError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    error = "USER_HAS_NO_PERMISSION"
    detail = "The requested operation cannot be performed by this user. Please, try again with the correct permissions."