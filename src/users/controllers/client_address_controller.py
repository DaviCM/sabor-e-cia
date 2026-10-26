from typing import Any
from brutils import is_valid_cep

from users.models import Client, ClientAddress
from users.errors import (
    ClientNotFoundError,
    InvalidCEPError,
    InvalidNumberError,
    AddressNotFoundError,
)

def create_client_address(current_client: Client, params: dict[str, Any]) -> ClientAddress:
    if current_client is None:
        raise ClientNotFoundError
    
    if not is_valid_cep(params["cep"]):
        raise InvalidCEPError
    
    if params["number"] <= 0:
        raise InvalidNumberError
    
    new_address = ClientAddress(
        cep=params["cep"],
        description=params["description"],
        number=params["number"],
        client=current_client,
    )
    
    new_address.save()
    
    return new_address


def list_client_addresses(current_client: Client):
    if current_client is None:
        raise ClientNotFoundError

    addresses = ClientAddress.objects.filter(client=current_client)

    if not addresses.exists():
        raise AddressNotFoundError

    return addresses


def update_client_address(current_client: Client, params: dict[str, Any]) -> ClientAddress:
    if current_client is None:
        raise ClientNotFoundError
    
    cep = params.get("cep")
    if (cep is not None) and not is_valid_cep(cep):
        raise InvalidCEPError
    
    number = params.get("number")
    if (number is not None) and (number <= 0):
        raise InvalidNumberError

    try:
        target_address = ClientAddress.objects.get(pk=params["id"], client=current_client)
    except ClientAddress.DoesNotExist:
        raise AddressNotFoundError
    
    if cep is not None:
        target_address.cep = cep
    
    description = params.get("description")
    if description is not None:
        target_address.description = description
    
    if number is not None:
        target_address.number = number
        
    target_address.save()
    
    return target_address


def delete_client_address(current_client: Client, target_address_id: int) -> None:
    if current_client is None:
        raise ClientNotFoundError

    try:
        target_address = ClientAddress.objects.get(pk=target_address_id, client=current_client)
    except ClientAddress.DoesNotExist:
        raise AddressNotFoundError

    target_address.delete()