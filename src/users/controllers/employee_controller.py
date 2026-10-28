from typing import Any

from brutils import is_valid_email, is_valid_cpf

from users.models import User, Employee, Roles
from users.controllers import email_already_exists, cpf_already_exists
from users.serializers import CreateEmployeeSerializer, UpdateEmployeeSerializer
from users.errors import *

def create_employee(params: dict[str, Any]) -> Employee:
    first_name = params.get("first_name")
    last_name = params.get("last_name")
    username = params.get("username")
    email = params.get("email")
    password = params.get("password")
    cpf = params.get("cpf")
    role = params.get("role")

    if is_valid_email(email) == False:
        raise InvalidEmailError
    
    if email_already_exists(email) == True:
        raise UserAlreadyExistsError
    
    if is_valid_cpf(cpf) == False:
        raise InvalidCPFError
    
    if cpf_already_exists(cpf) == True:
        raise UserAlreadyExistsError
    
    new_employee = Employee(
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            extra_fields={
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": True,
            },
        ),
        cpf=cpf,
        role=role
    )

    new_employee.save()
    
    return new_employee


def update_employee(current_employee: Employee, params: dict[str, Any]) -> Employee:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    first_name = params.get("first_name")
    last_name = params.get("last_name")
    username = params.get("username")
    email = params.get("email")
    password = params.get("password")
    cpf = params.get("cpf")
    role = params.get("role")

    try:
        target_employee = Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        raise EmployeeNotFoundError
    
    if current_employee.user.is_admin == False:
        raise UserHasNoPermissionError
    
    if (email != None) and (is_valid_email(email=email) == False):
        raise InvalidEmailError
    
    if (email != None) and (email_already_exists(email=email) == True):
        raise UserAlreadyExistsError
    
    if (cpf != None) and (is_valid_cpf(cpf) == False):
        raise InvalidCPFError
    
    if (cpf != None) and (cpf_already_exists(cpf) == True):
        raise UserAlreadyExistsError
    
    if (role != None) and (role not in Roles):
        raise InvalidRoleError

    target_user = target_employee.user
    
    if first_name != None:
        target_user.first_name = first_name
        
    if last_name != None:
        target_user.last_name = last_name
        
    if username != None:
        target_user.username = username
            
    if email != None:
        target_user.email = email
        
    if password != None:
        target_user.set_password(password)
        
    if cpf != None:
        target_user.cpf = cpf
        
    if role != None:
        target_employee.role = role
        
    target_user.save()
    target_employee.save()
    
    return target_employee
            

def delete_employee(current_employee: Employee, target_employee_id: int) -> None:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_employee = Employee.objects.get(pk=target_employee_id)
    except Employee.DoesNotExist:
        raise EmployeeNotFoundError
    
    target_user = target_employee.user
    target_user.delete()
    

