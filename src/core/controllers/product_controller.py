from typing import Any

from core.models import Product
from core.serializers import CreateProductSerializer, UpdateProductSerializer, QueryProductSerializer
from core.errors import InvalidValueError, ProductNotFoundError
from users.models import Employee, User
from users.errors import EmployeeNotFoundError, UserNotFoundError, UserHasNoPermissionError

def create_product(current_employee: Employee, params: dict[str, Any]) -> Product:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    description = params.get("description")
    category = params.get("category")
    value = params.get("value")

    if value < 0:
        raise InvalidValueError

    new_product = Product(
        description=description,
        category=category,
        value=value
    )

    new_product.save()

    return new_product


def list_products(current_user: User, params: dict[str, Any]):
    if current_user == None:
        raise UserNotFoundError
    
    id = params.get("id")
    description = params.get("description")
    category = params.get("category")
    minimum_value = params.get("minimum_value")
    maximum_value = params.get("maximum_value")

    if minimum_value > maximum_value:
        raise InvalidValueError

    products = Product.objects.all()

    if id != None:
        products = products.filter(pk=id)

    if description != None:
        products = products.filter(description__icontains=description)

    if category != None:
        products = products.filter(category=category)

    if minimum_value != None:
        products = products.filter(value__gte=minimum_value)

    if maximum_value != None:
        products = products.filter(value__lte=maximum_value)

    if products.exists() == False:
        raise ProductNotFoundError

    return products


def update_product(current_employee: Employee, params: dict[str, Any]) -> Product:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    id = params.get("id")
    description = params.get("description")
    category = params.get("category")
    value = params.get("value")

    try:
        target_product = Product.objects.get(pk=id)
    except Product.DoesNotExist:
        raise ProductNotFoundError

    if (value != None) and (value < 0):
        raise InvalidValueError

    if description != None:
        target_product.description = description

    if category != None:
        target_product.category = category

    if value != None:
        target_product.value = value

    target_product.save()

    return target_product


def delete_product(current_employee: Employee, target_product_id: int) -> None:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_product = Product.objects.get(pk=target_product_id)
    except Product.DoesNotExist:
        raise ProductNotFoundError

    target_product.delete()