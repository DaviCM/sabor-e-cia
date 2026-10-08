from brutils import is_valid_cep

from users.models import Client, ClientAddress
from users.serializers import CreateAddressSerializer, UpdateAddressSerializer
from users.errors import *

def create_client_address(current_client: Client, params: CreateAddressSerializer) -> ClientAddress:
    if current_client == None:
        raise UserNotFoundError
    
    if is_valid_cep(params.cep) == False:
        raise InvalidCEPError
    
    if params.number <= 0:
        raise InvalidNumberError
    
    new_address = ClientAddress(
        cep=params.cep,
        description=params.description,
        numbers=params.number,
        creator=current_client
    )
    
    new_address.save()
    
    return new_address


def list_client_addresses(current_client: Client):
    if current_client == None:
        raise UserNotFoundError


def update_client_address(current_client: Client, target_address_id: int, params: UpdateAddressSerializer) -> ClientAddress:
    if current_client == None:
        raise UserNotFoundError
    
    if (params.cep != None) and (is_valid_cep(params.cep) == False):
        raise InvalidCEPError
    
    if params.number <= 0:
        raise InvalidNumberError
    
    target_address: ClientAddress = ClientAddress.objects.filter(pk=target_address_id)
    
    if params.cep != None:
        target_address.cep = params.cep
    
    if params.description != None:
        target_address.description = params.description
    
    if params.number != None:
        target_address.number = params.number
        
    target_address.save()
    
    return target_address


def delete_client_address(current_client: Client, target_address_id: int):
    if current_client == None:
        raise UserNotFoundError
    
    target_address = ClientAddress.objects.filter(pk=target_address_id)
    target_address.delete()