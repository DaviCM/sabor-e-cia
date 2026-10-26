from typing import Any
from brutils import is_valid_email, is_valid_phone

from users.models import User, Client
from users.controllers.user_creation_verifiers import email_already_exists
from users.errors import (
    ClientNotFoundError,
    InvalidEmailError,
    UserAlreadyExistsError,
    InvalidPhoneError,
)

def create_client(params: dict[str, Any]) -> Client:
    if not is_valid_email(params["email"]):
        raise InvalidEmailError
    
    if email_already_exists(params["email"]):
        raise UserAlreadyExistsError
    
    if not is_valid_phone(params["phone"]):
        raise InvalidPhoneError
    
    created_user = User.objects.create_user(
        username=params["username"],
        email=params["email"],
        password=params["password"],
        first_name=params.get("first_name", ""),
        last_name=params.get("last_name", ""),
        is_staff=False,
    )

    new_client = Client(
        user=created_user,
        phone=params["phone"],
    )
    new_client.save()
    
    return new_client


def update_client(current_client: Client, params: dict[str, Any]) -> Client:
    if current_client is None:
        raise ClientNotFoundError
    
    current_user: User = current_client.user
    email = params.get("email")

    if email is not None:
        if not is_valid_email(email):
            raise InvalidEmailError
        if (email != current_user.email) and email_already_exists(email):
            raise UserAlreadyExistsError
    
    phone = params.get("phone")
    if (phone is not None) and not is_valid_phone(phone):
        raise InvalidPhoneError
    
    first_name = params.get("first_name")
    if first_name is not None:
        current_user.first_name = first_name
        
    last_name = params.get("last_name")
    if last_name is not None:
        current_user.last_name = last_name
        
    username = params.get("username")
    if username is not None:
        current_user.username = username
            
    if email is not None:
        current_user.email = email
        
    password = params.get("password")
    if password is not None:
        current_user.set_password(password)
        
    if phone is not None:
        current_client.phone = phone
        
    current_user.save()
    current_client.save()
    
    return current_client
            

def delete_client(current_client: Client) -> None:
    if current_client is None:
        raise ClientNotFoundError
    
    current_user: User = current_client.user
    current_user.delete()