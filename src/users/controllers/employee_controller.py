from typing import Any
from brutils import is_valid_email, is_valid_cpf

from users.models import User, Employee, Roles
from users.controllers.user_creation_verifiers import email_already_exists, cpf_already_exists
from users.errors import (
    EmployeeNotFoundError,
    UserHasNoPermissionError,
    InvalidEmailError,
    InvalidCPFError,
    UserAlreadyExistsError,
    InvalidRoleError,
)

def create_employee(params: dict[str, Any]) -> Employee:
    if not is_valid_email(params["email"]):
        raise InvalidEmailError
    
    if email_already_exists(params["email"]):
        raise UserAlreadyExistsError
    
    if not is_valid_cpf(params["cpf"]):
        raise InvalidCPFError
    
    if cpf_already_exists(params["cpf"]):
        raise UserAlreadyExistsError

    role = params["role"]
    valid_roles = [r.value for r in Roles]
    if role not in valid_roles and role not in Roles:
        raise InvalidRoleError
    role_val = role.value if isinstance(role, Roles) else role
    
    created_user = User.objects.create_user(
        username=params["username"],
        email=params["email"],
        password=params["password"],
        first_name=params.get("first_name", ""),
        last_name=params.get("last_name", ""),
        is_staff=True,
    )

    new_employee = Employee(
        user=created_user,
        cpf=params["cpf"],
        role=role_val,
    )
    new_employee.save()
    
    return new_employee


def update_employee(current_employee: Employee, params: dict[str, Any]) -> Employee:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_employee = Employee.objects.get(pk=params["id"])
    except Employee.DoesNotExist:
        raise EmployeeNotFoundError
    
    # No Django padrão, administradores possuem is_superuser=True
    is_admin = getattr(current_employee.user, "is_admin", current_employee.user.is_superuser)
    if not is_admin:
        raise UserHasNoPermissionError
    
    target_user = target_employee.user

    email = params.get("email")
    if email is not None:
        if not is_valid_email(email):
            raise InvalidEmailError
        if (email != target_user.email) and email_already_exists(email):
            raise UserAlreadyExistsError
    
    cpf = params.get("cpf")
    if cpf is not None:
        if not is_valid_cpf(cpf):
            raise InvalidCPFError
        if (cpf != target_employee.cpf) and cpf_already_exists(cpf):
            raise UserAlreadyExistsError
    
    role = params.get("role")
    valid_roles = [r.value for r in Roles]
    if (role is not None) and (role not in valid_roles and role not in Roles):
        raise InvalidRoleError
    
    first_name = params.get("first_name")
    if first_name is not None:
        target_user.first_name = first_name
        
    last_name = params.get("last_name")
    if last_name is not None:
        target_user.last_name = last_name
        
    username = params.get("username")
    if username is not None:
        target_user.username = username
            
    if email is not None:
        target_user.email = email
        
    password = params.get("password")
    if password is not None:
        target_user.set_password(password)
        
    if cpf is not None:
        target_employee.cpf = cpf
        
    if role is not None:
        target_employee.role = role.value if isinstance(role, Roles) else role
        
    target_user.save()
    target_employee.save()
    
    return target_employee
            

def delete_employee(current_employee: Employee, target_employee_id: int) -> None:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    is_admin = getattr(current_employee.user, "is_admin", current_employee.user.is_superuser)
    if not is_admin:
        raise UserHasNoPermissionError

    try:
        target_employee = Employee.objects.get(pk=target_employee_id)
    except Employee.DoesNotExist:
        raise EmployeeNotFoundError
    
    target_user: User = target_employee.user
    target_user.delete()
