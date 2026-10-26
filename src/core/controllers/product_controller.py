from typing import Any
from core.models import Product
from core.errors import InvalidValueError, ProductNotFoundError
from users.models import Employee, User
from users.errors import EmployeeNotFoundError, UserNotFoundError, UserHasNoPermissionError

def create_product(current_employee: Employee, params: dict[str, Any]) -> Product:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    if params["value"] < 0:
        raise InvalidValueError

    new_product = Product(
        description=params["description"],
        category=params["category"],
        value=params["value"]
    )

    new_product.save()

    return new_product


def list_products(current_user: User, params: dict[str, Any]):
    if current_user is None:
        raise UserNotFoundError

    minimum_value = params.get("minimum_value")
    maximum_value = params.get("maximum_value")

    if (minimum_value is not None) and (maximum_value is not None):
        if minimum_value > maximum_value:
            raise InvalidValueError

    products = Product.objects.all()

    description = params.get("description")
    if description is not None:
        products = products.filter(description__icontains=description)

    category = params.get("category")
    if category is not None:
        products = products.filter(category=category)

    if minimum_value is not None:
        products = products.filter(value__gte=minimum_value)

    if maximum_value is not None:
        products = products.filter(value__lte=maximum_value)

    if not products.exists():
        raise ProductNotFoundError

    return products


def update_product(current_employee: Employee, params: dict[str, Any]) -> Product:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_product = Product.objects.get(pk=params["id"])
    except Product.DoesNotExist:
        raise ProductNotFoundError

    value = params.get("value")
    if (value is not None) and (value < 0):
        raise InvalidValueError

    description = params.get("description")
    if description is not None:
        target_product.description = description

    category = params.get("category")
    if category is not None:
        target_product.category = category

    if value is not None:
        target_product.value = value

    target_product.save()

    return target_product


def delete_product(current_employee: Employee, target_product_id: int) -> None:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_product = Product.objects.get(pk=target_product_id)
    except Product.DoesNotExist:
        raise ProductNotFoundError

    target_product.delete()