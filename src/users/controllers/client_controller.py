from typing import Any

from brutils import is_valid_email, is_valid_phone

from users.models import User, Client
from users.controllers import email_already_exists
from users.serializers import CreateClientSerializer, UpdateClientSerializer
from users.errors import *

def create_client(params: dict[str, Any]) -> Client:
    first_name = params.get("first_name")
    last_name = params.get("last_name")
    username = params.get("username")
    email = params.get("email")
    password = params.get("password")
    phone = params.get("phone")

    if is_valid_email(email) == False:
        raise InvalidEmailError
    
    if email_already_exists(email) == True:
        raise UserAlreadyExistsError
    
    if is_valid_phone(phone) == False:
        raise InvalidPhoneError
    
    new_client = Client(
        user=User.objects.create_user(
            username=username,
            email=email,
            password=password,
            extra_fields={
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": False,
            },
        ),
        phone=phone,
    )

    new_client.save()
    
    return new_client


def update_client(current_client: Client, params: UpdateClientSerializer) -> Client:
    if current_client == None:
        raise ClientNotFoundError

    id = params.get("id")
    first_name = params.get("first_name")
    last_name = params.get("last_name")
    username = params.get("username")
    email = params.get("email")
    password = params.get("password")
    phone = params.get("phone")
    
    if (email != None) and (is_valid_email(email=email) == False):
        raise InvalidEmailError
    
    if (email != None) and (email_already_exists(email=email) == True):
        raise UserAlreadyExistsError
    
    if (phone != None) and (is_valid_phone(phone) == False):
        raise InvalidPhoneError
    
    current_user: User = current_client.user
    
    if first_name != None:
        current_user.first_name = first_name
        
    if last_name != None:
        current_user.last_name = last_name
        
    if username != None:
        current_user.username = username
            
    if email != None:
        current_user.email = email
        
    if password != None:
        current_user.set_password(password)
        
    if phone != None:
        current_client.phone = phone
        
    current_user.save()
    current_client.save()
    
    return current_client
            

def delete_client(current_client: Client) -> None:
    if current_client == None:
        raise ClientNotFoundError
    
    current_user: User = current_client.user
    current_user.delete()