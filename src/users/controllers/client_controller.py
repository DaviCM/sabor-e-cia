from brutils import is_valid_email, is_valid_phone

from users.models import User, Client, ClientAddress
from users.controllers import email_already_exists
from users.serializers import CreateClientSerializer, UpdateClientSerializer, CreateAddressSerializer, UpdateAddressSerializer
from users.errors import *

def create_client(params: CreateClientSerializer) -> Client:
    if is_valid_email(params.email) == False:
        raise InvalidEmailError
    
    if email_already_exists(params.email) == True:
        raise UserAlreadyExistsError
    
    if is_valid_phone(params.phone) == False:
        raise InvalidPhoneError
    
    new_client = Client(
        user=User.objects.create_user(
            username=params.username,
            email=params.email,
            password=params.password,
            extra_fields={
                "first_name": params.first_name,
                "last_name": params.last_name,
            },
        ),
        phone=params.phone,
    )

    new_client.save()
    
    return new_client


def update_client(current_client: Client, params: UpdateClientSerializer) -> Client:
    if current_client == None:
        raise UserNotFoundError
    
    if (params.email != None) and (is_valid_email(email=params.email) == False):
        raise InvalidEmailError
    
    if (params.email != None) and (email_already_exists(email=params.email) == True):
        raise UserAlreadyExistsError
    
    if (params.phone != None) and (is_valid_phone(params.phone) == False):
        raise InvalidPhoneError
    
    current_user: User = current_client.user
    
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
        
    if params.phone != None:
        current_client.phone = params.phone
        
    current_user.save()
    current_client.save()
    
    return current_client
            

def delete_client(current_client: Client):
    if current_client == None:
        raise UserNotFoundError
    
    current_user: User = current_client.user
    current_user.delete()