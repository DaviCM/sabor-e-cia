from core.models import Product
from core.serializers import CreateProductSerializer, UpdateProductSerializer, QueryProductSerializer
from core.errors import InvalidValueError, ProductNotFoundError
from users.models import Employee, User
from users.errors import EmployeeNotFoundError, UserNotFoundError, UserHasNoPermissionError

def create_product(current_employee: Employee, params: CreateProductSerializer) -> Product:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if params.value < 0:
        raise InvalidValueError

    new_product = Product(
        description=params.description,
        category=params.category,
        value=params.value
    )

    new_product.save()

    return new_product


def list_products(current_user: User, params: QueryProductSerializer):
    if current_user == None:
        raise UserNotFoundError

    if params.minimum_value > params.maximum_value:
        raise InvalidValueError

    products = Product.objects.all()

    if params.description != None:
        products = products.filter(description__icontains=params.description)

    if params.category != None:
        products = products.filter(category=params.category)

    if params.minimum_value != None:
        products = products.filter(value__gte=params.minimum_value)

    if params.maximum_value != None:
        products = products.filter(value__lte=params.maximum_value)

    if products.exists() == False:
        raise ProductNotFoundError

    return products


def update_product(current_employee: Employee, params: UpdateProductSerializer) -> Product:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_product = Product.objects.get(pk=params.id)
    except Product.DoesNotExist:
        raise ProductNotFoundError

    if (params.value != None) and (params.value < 0):
        raise InvalidValueError

    if params.description != None:
        target_product.description = params.description

    if params.category != None:
        target_product.category = params.category

    if params.value != None:
        target_product.value = params.value

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