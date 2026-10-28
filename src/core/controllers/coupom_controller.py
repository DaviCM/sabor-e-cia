from typing import Any

from core.models import Coupom
from core.serializers import CreateCoupomSerializer, UpdateCoupomSerializer, QueryCoupomSerializer
from core.errors import InvalidMultiplierError, InvalidDateError, CoupomNotFoundError
from users.models import Employee
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError

def create_coupom(current_employee: Employee, params: CreateCoupomSerializer) -> Coupom:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if params.multiplier < 1:
        raise InvalidMultiplierError

    new_coupom = Coupom(
        token=params.token,
        multiplier=params.multiplier,
        expires_at=params.expires_at,
    )

    new_coupom.save()

    if params.products != None:
        for product in params.products:
            # add() adiciona uma entrada, nesse caso via PK, a um relacionamento many-to-many.
            new_coupom.products.add(product)

    return new_coupom


def list_coupoms(current_employee: Employee, params: QueryCoupomSerializer):
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if (params.minimum_multiplier != None) and (params.minimum_multiplier < 1):
        raise InvalidMultiplierError
        
    if (params.maximum_multiplier != None) and (params.maximum_multiplier < 1):
        raise InvalidMultiplierError

    if (params.created_before != None) and (params.created_after != None):
        if params.created_after < params.created_before:
            raise InvalidDateError
            
    if (params.expires_before != None) and (params.expires_after != None):
        if params.expires_after < params.expires_before:
            raise InvalidDateError
    
    coupoms = Coupom.objects.all()

    if params.token != None:
        coupoms = coupoms.filter(token__icontains=params.token)

    if params.minimum_multiplier != None:
        coupoms = coupoms.filter(multiplier__gte=params.minimum_multiplier)

    if params.maximum_multiplier != None:
        coupoms = coupoms.filter(multiplier__lte=params.maximum_multiplier)

    if params.created_before != None:
        coupoms = coupoms.filter(created_at__gte=params.created_before)

    if params.created_after != None:
        coupoms = coupoms.filter(created_at__lte=params.created_after)

    if params.expires_before != None:
        coupoms = coupoms.filter(expires_at__gte=params.expires_before)

    if params.expires_after != None:
        coupoms = coupoms.filter(expires_at__lte=params.expires_after)

    if params.product_id != None:
        coupoms = coupoms.filter(products__pk=params.product_id)

    if coupoms.exists() == False:
        raise CoupomNotFoundError
    
    return coupoms


def update_coupom(current_employee: Employee, params: UpdateCoupomSerializer) -> Coupom:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if (params.multiplier != None) and (params.multiplier < 1):
        raise InvalidMultiplierError

    try:
        target_coupom = Coupom.objects.get(pk=params.id)
    except Coupom.DoesNotExist:
        raise CoupomNotFoundError

    if (params.expires_at != None) and (target_coupom.created_at >= params.expires_at):
        raise InvalidDateError
    
    if params.token != None:
        target_coupom.token = params.token

    if params.multiplier != None:
        target_coupom.multiplier = params.multiplier

    if params.expires_at != None:
        target_coupom.expires_at = params.expires_at

    if params.products != None:
        for product in params.products:
            if target_coupom.exists(products__pk=product) == False:
                target_coupom.products.add(product)

    target_coupom.save()

    return target_coupom


def delete_coupom(current_employee: Employee, target_coupom_id: int) -> None:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_coupom = Coupom.objects.get(pk=target_coupom_id)
    except Coupom.DoesNotExist:
        raise CoupomNotFoundError
    
    target_coupom.delete()