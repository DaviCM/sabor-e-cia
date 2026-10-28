from typing import Any

from core.models import Order, Product, Coupom, ProductsOrders
from core.serializers import CreateOrderSerializer, QueryOrderSerializer, UpdateOrderStatusSerializer
from core.errors import OrderNotFoundError, ProductNotFoundError, InvalidValueError, InvalidTotalValueError, InvalidOrderDateError, InvalidQuantitiesError
from users.models import Client, Employee
from users.errors import ClientNotFoundError, EmployeeNotFoundError, UserHasNoPermissionError

def create_order(current_client: Client, current_employee: Employee, params: dict[str, Any]) -> Order:
    if current_client == None:
        raise ClientNotFoundError

    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError

    id = params.get("id")
    datetime = params.get("datetime")
    quantity = params.get("quantity")
    total_value = params.get("total_value")
    category = params.get("category")
    status = params.get("status")
    cover = params.get("cover")
    notes = params.get("notes")

    client_id = params.get("client_id")
    employee_id = params.get("employee_id")

    products = params.get("products")
    coupoms = params.get("coupoms")

    if products == None:
        raise ProductNotFoundError

    if quantity < 1:
        raise InvalidQuantitiesError

    if total_value < 0:
        raise InvalidTotalValueError

    if (cover != None) and (cover < 0):
        raise InvalidValueError

    new_order = Order(
        quantity=quantity,
        total_value=total_value,
        category=category,
        status=status,
        cover=cover,
        notes=notes,

        client=current_client,
        employee=current_employee,
    )

    for product_entry in products:
        # O resultado de "products" é uma lista de dicionários, com as informações
        # que foram passadas para cada membro do pedido.

        # Associamos o pedido na hora, pois ele ainda não existe no banco para ser passado como parâmetro.
        is_combo = product_entry.get("is_combo")
        product_type = product_entry.get("product_type")
        product = product_entry.get("product")

        new_entry = ProductsOrders(
            product_type=product_type,
            is_combo=is_combo,

            product=product,
            order=new_order,
        )

        new_order.products.add(new_entry)

    if (coupoms != None):
        for coupom in coupoms:
            new_order.coupoms.add(coupom)

    new_order.save()

    return new_order


def client_list_orders(current_client: Client, params: dict[str, Any]):
    if current_client == None:
        raise ClientNotFoundError

    id = params.get("id")
    minimum_date = params.get("minimum_date")
    maximum_date = params.get("maximum_date")
    minimum_quantity = params.get("minimum_quantity")
    maximum_quantity = params.get("maximum_quantity")
    minimum_value = params.get("minimum_value")
    maximum_value = params.get("maximum_value")
    category = params.get("category")
    status = params.get("status")
    notes = params.get("notes")

    if (minimum_date != None) and (maximum_date != None):
        if minimum_date > maximum_date:
            raise InvalidOrderDateError

    if (minimum_quantity != None) and (minimum_quantity < 0):
        raise InvalidQuantitiesError

    if (maximum_quantity != None) and (maximum_quantity < 0):
        raise InvalidQuantitiesError

    if (minimum_quantity != None) and (maximum_quantity != None):
        if minimum_quantity > maximum_quantity:
            raise InvalidQuantitiesError

    if (minimum_value != None) and (minimum_value < 0):
        raise InvalidValueError

    if (maximum_value != None) and (maximum_value < 0):
        raise InvalidValueError

    if (minimum_value != None) and (maximum_value != None):
        if minimum_value > maximum_value:
            raise InvalidValueError

    orders = Order.objects.filter(client=current_client)

    if id != None:
        orders = orders.filter(pk=id)

    if minimum_date != None:
        orders = orders.filter(datetime__gte=minimum_date)

    if maximum_date != None:
        orders = orders.filter(datetime__lte=maximum_date)

    if minimum_quantity != None:
        orders = orders.filter(quantity__gte=minimum_quantity)
    
    if maximum_quantity != None:
        orders = orders.filter(quantity__lte=maximum_quantity)

    if minimum_value != None:
        orders = orders.filter(total_value__gte=minimum_value)
    
    if maximum_value != None:
        orders = orders.filter(total_value__lte=maximum_value)

    if category != None:
        orders = orders.filter(category=category)

    if status != None:
        orders = orders.filter(status=status)

    if notes != None:
        orders = orders.filter(notes__icontains=notes)


def employee_list_orders(current_employee: Employee, params: dict[str, Any]):
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError


def update_order_status(current_employee: Employee, params: dict[str, Any]) -> Order:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError

    id = params.get("id")
    status = params.get("status")

    try:
        target_order = Order.objects.get(pk=id)
    except Order.DoesNotExist:
        raise OrderNotFoundError

    target_order.status = status

    target_order.save()

    return target_order
