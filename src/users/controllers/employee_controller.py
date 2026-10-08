from brutils import is_valid_email, is_valid_cpf

from users.models import User, Employee, Roles
from users.controllers import email_already_exists, cpf_already_exists
from users.serializers import CreateEmployeeSerializer, UpdateEmployeeSerializer
from users.errors import *

def create_employee(params: CreateEmployeeSerializer) -> Employee:
    if is_valid_email(params.email) == False:
        raise InvalidEmailError
    
    if email_already_exists(params.email) == True:
        raise UserAlreadyExistsError
    
    if is_valid_cpf(params.cpf) == False:
        raise InvalidCPFError
    
    if cpf_already_exists(params.cpf) == True:
        raise UserAlreadyExistsError
    
    new_employee = Employee(
        user=User.objects.create_user(
            username=params.username,
            email=params.email,
            password=params.password,
            extra_fields={
                "first_name": params.first_name,
                "last_name": params.last_name,
            },
        ),
        cpf=params.cpf,
        role=params.role
    )

    new_employee.save()
    
    return new_employee


def update_employee(current_employee: Employee, params: UpdateEmployeeSerializer) -> Employee:
    if current_employee == None:
        raise UserNotFoundError
    
    if (params.email != None) and (is_valid_email(email=params.email) == False):
        raise InvalidEmailError
    
    if (params.email != None) and (email_already_exists(email=params.email) == True):
        raise UserAlreadyExistsError
    
    if (params.cpf != None) and (is_valid_cpf(params.cpf) == False):
        raise InvalidCPFError
    
    if (params.cpf != None) and (cpf_already_exists(params.cpf) == True):
        raise UserAlreadyExistsError
    
    if (params.role != None) and (params.role not in Roles):
        raise InvalidRoleError
    
    current_user: User = current_employee.user
    
    if params.first_name != None:
        current_user.first_name = params.first_name
        
    if params.last_name != None:
        current_user.last_name = params.last_name
        
    if params.username != None:
        current_user.username = params.username
            
    if params.email != None:
        current_user.email = params.email
        
    if params.password != None:
        current_user.set_password(params.password)
        
    if params.cpf != None:
        current_employee.cpf = params.cpf
        
    if params.role != None:
        current_employee.role = params.role
        
    current_user.save()
    current_employee.save()
    
    return current_employee
            

def delete_employee(current_employee: Employee):
    if current_employee == None:
        raise UserNotFoundError
    
    current_user: User = current_employee.user
    current_user.delete()
    

