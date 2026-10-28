from typing import Any
from core.models import Coupom
from core.errors import InvalidMultiplierError, InvalidCoupomDateError, CoupomNotFoundError
from users.models import Employee
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError

def create_coupom(current_employee: Employee, params: dict[str, Any]) -> Coupom:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    if params["multiplier"] < 1:
        raise InvalidMultiplierError

    new_coupom = Coupom(
        token=params["token"],
        multiplier=params["multiplier"],
        expires_at=params["expires_at"],
    )

    new_coupom.save()

    if params.get("products") is not None:
        for product in params["products"]:
            new_coupom.products.add(product)

    return new_coupom


def list_coupoms(current_employee: Employee, params: dict[str, Any]):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    minimum_multiplier = params.get("minimum_multiplier")
    maximum_multiplier = params.get("maximum_multiplier")
    created_before = params.get("created_before")
    created_after = params.get("created_after")
    expires_before = params.get("expires_before")
    expires_after = params.get("expires_after")

    if (minimum_multiplier is not None) and (minimum_multiplier < 1):
        raise InvalidMultiplierError
        
    if (maximum_multiplier is not None) and (maximum_multiplier < 1):
        raise InvalidMultiplierError

    if (minimum_multiplier is not None) and (maximum_multiplier is not None):
        if minimum_multiplier > maximum_multiplier:
            raise InvalidMultiplierError

    if (created_before is not None) and (created_after is not None):
        if created_after > created_before:
            raise InvalidCoupomDateError
            
    if (expires_before is not None) and (expires_after is not None):
        if expires_after > expires_before:
            raise InvalidCoupomDateError
    
    coupoms = Coupom.objects.all()

    token = params.get("token")
    if token is not None:
        coupoms = coupoms.filter(token__icontains=token)

    if minimum_multiplier is not None:
        coupoms = coupoms.filter(multiplier__gte=minimum_multiplier)

    if maximum_multiplier is not None:
        coupoms = coupoms.filter(multiplier__lte=maximum_multiplier)

    if created_before is not None:
        coupoms = coupoms.filter(created_at__lte=created_before)

    if created_after is not None:
        coupoms = coupoms.filter(created_at__gte=created_after)

    if expires_before is not None:
        coupoms = coupoms.filter(expires_at__lte=expires_before)

    if expires_after is not None:
        coupoms = coupoms.filter(expires_at__gte=expires_after)

    product_id = params.get("product_id")
    if product_id is not None:
        coupoms = coupoms.filter(products__pk=product_id)

    if not coupoms.exists():
        raise CoupomNotFoundError
    
    return coupoms


def update_coupom(current_employee: Employee, params: dict[str, Any]) -> Coupom:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    multiplier = params.get("multiplier")
    if (multiplier is not None) and (multiplier < 1):
        raise InvalidMultiplierError

    try:
        target_coupom = Coupom.objects.get(pk=params["id"])
    except Coupom.DoesNotExist:
        raise CoupomNotFoundError

    expires_at = params.get("expires_at")
    if (expires_at is not None) and (target_coupom.created_at >= expires_at):
        raise InvalidCoupomDateError
    
    token = params.get("token")
    if token is not None:
        target_coupom.token = token

    if multiplier is not None:
        target_coupom.multiplier = multiplier

    if expires_at is not None:
        target_coupom.expires_at = expires_at

    products = params.get("products")
    if products is not None:
        for product in products:
            product_pk = product.pk if hasattr(product, "pk") else product
            if not target_coupom.products.filter(pk=product_pk).exists():
                target_coupom.products.add(product)

    target_coupom.save()

    return target_coupom


def delete_coupom(current_employee: Employee, target_coupom_id: int) -> None:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_coupom = Coupom.objects.get(pk=target_coupom_id)
    except Coupom.DoesNotExist:
        raise CoupomNotFoundError
    
    target_coupom.delete()
