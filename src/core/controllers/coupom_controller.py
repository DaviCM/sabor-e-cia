from core.models import Coupom, Product
from core.serializers import CreateCoupomSerializer, UpdateCoupomSerializer, QueryCoupomSerializer
from core.errors import InvalidMultiplierError, InvalidDateError, CoupomNotFoundError
from users.models import Employee, User
from users.errors import UserNotFoundError, UserHasNoPermissionError

def create_coupom(current_employee: Employee, params: CreateCoupomSerializer) -> Coupom:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if params.multiplier < 1:
        raise InvalidMultiplierError

    if params.expires_at >= params.created_at:
        raise InvalidDateError

    new_coupom = Coupom(
        token=params.token,
        multiplier=params.multiplier,
        created_at=params.created_at,
        expires_at=params.expires_at,
    )

    new_coupom.save()

    return new_coupom


def list_coupoms(current_employee: Employee, params: QueryCoupomSerializer):
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if (params.minimum_multiplier != None) and (params.minimum_multiplier < 1):
        raise InvalidMultiplierError
        
    if (params.maximum_multiplier != None) and (params.maximum_multiplier < 1):
        raise InvalidMultiplierError

    coupoms = Coupom.objects.all()

    if params.token != None:
        coupoms = coupoms.filter(token__icontains=params.token)

    if params.minimum_multiplier != None:
        coupoms = coupoms.filter(multiplier__gte=params.minimum_multiplier)

    if params.maximum_multiplier != None:
        coupoms = coupoms.filter(multiplier__lte=params.maximum_multiplier)

    # ! FINALIZAR AS VERIFICAÇÕES PARA O SERIALIZADOR

    if params.created_after < params.created_before:
        raise InvalidDateError

    if params.expires_after < params.expires_before:
        raise InvalidDateError





def update_coupom(current_employee: Employee, params: UpdateCoupomSerializer) -> Coupom:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError


def delete_coupom(current_employee: Employee, params: CreateCoupomSerializer) -> None:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError