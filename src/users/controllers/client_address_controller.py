from typing import Any

from brutils import is_valid_cep

from users.models import Client, ClientAddress
from users.serializers import CreateAddressSerializer, UpdateAddressSerializer
from users.errors import *

def create_client_address(current_client: Client, params: dict[str, Any]) -> ClientAddress:
    if current_client == None:
        raise ClientNotFoundError

    description = params.get("description")
    number = params.get("number")
    cep = params.get("cep")
    
    if is_valid_cep(cep) == False:
        raise InvalidCEPError
    
    if number <= 0:
        raise InvalidNumberError
    
    new_address = ClientAddress(
        cep=cep,
        description=description,
        number=number,
        creator=current_client
    )
    
    new_address.save()
    
    return new_address


def list_client_addresses(current_client: Client):
    if current_client == None:
        raise ClientNotFoundError

    addresses = ClientAddress.objects.filter(client=current_client)

    if addresses.exists() == False:
        raise AddressNotFoundError

    return addresses


def update_client_address(current_client: Client, params: dict[str, Any]) -> ClientAddress:
    if current_client == None:
        raise ClientNotFoundError

    id = params.get("id")
    description = params.get("description")
    number = params.get("number")
    cep = params.get("cep")
    
    if (cep != None) and (is_valid_cep(cep) == False):
        raise InvalidCEPError
    
    if number <= 0:
        raise InvalidNumberError

    try:
        target_address = ClientAddress.objects.get(pk=id)
    except ClientAddress.DoesNotExist:
        raise AddressNotFoundError
    
    if cep != None:
        target_address.cep = cep
    
    if description != None:
        target_address.description = description
    
    if number != None:
        target_address.number = number
        
    target_address.save()
    
    return target_address



def delete_client_address(current_client: Client, target_address_id: int) -> None:
    if current_client == None:
        raise ClientNotFoundError

    try:
        target_address = ClientAddress.objects.get(pk=target_address_id)
    except Client.DoesNotExist:
        raise AddressNotFoundError

    target_address.delete()