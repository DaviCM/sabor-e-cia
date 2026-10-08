from rest_framework import status

class AppError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error = "INTERNAL_SERVER_ERROR" 
    detail = "Um erro de servidor ocorreu. Por favor, contate a administração do sistema."