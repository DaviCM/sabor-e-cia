from typing import Any
from core.models import Order, ProductsOrders
from core.errors import OrderNotFoundError, InvalidValueError, InvalidTotalValueError, InvalidOrderDateError, InvalidQuantitiesError
from users.models import Client, Employee
from users.errors import ClientNotFoundError, EmployeeNotFoundError, UserHasNoPermissionError

def create_order(current_client: Client, current_employee: Employee, params: dict[str, Any]) -> Order:
    if current_client is None:
        raise ClientNotFoundError

    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    if params["quantity"] < 1:
        raise InvalidQuantitiesError

    if params["total_value"] < 0:
        raise InvalidTotalValueError

    cover = params.get("cover")
    if (cover is not None) and (cover < 0):
        raise InvalidValueError

    new_order = Order(
        quantity=params["quantity"],
        total_value=params["total_value"],
        category=params["category"],
        status=params["status"],
        cover=cover,
        notes=params.get("notes"),

        client=current_client,
        employee=current_employee,
    )
    new_order.save()

    for product_entry in params.get("products", []):
        new_entry = ProductsOrders(
            product_type=product_entry["product_type"],
            is_combo=product_entry.get("is_combo", False),

            product=product_entry["product"],
            order=new_order,
        )
        new_entry.save()

    coupoms = params.get("coupoms")
    if coupoms is not None:
        for coupom in coupoms:
            new_order.coupoms.add(coupom)

    return new_order


def client_list_orders(current_client: Client, params: dict[str, Any] | Any):
    if current_client is None:
        raise ClientNotFoundError

    data = params.validated_data if hasattr(params, "validated_data") else params

    minimum_date = data.get("minimum_date")
    maximum_date = data.get("maximum_date")
    minimum_quantity = data.get("minimum_quantity")
    maximum_quantity = data.get("maximum_quantity")
    minimum_value = data.get("minimum_value")
    maximum_value = data.get("maximum_value")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidOrderDateError

    if (minimum_quantity is not None) and (maximum_quantity is not None):
        if minimum_quantity > maximum_quantity:
            raise InvalidQuantitiesError

    if (minimum_value is not None) and (maximum_value is not None):
        if minimum_value > maximum_value:
            raise InvalidValueError

    orders = Order.objects.filter(client=current_client)

    if minimum_date is not None:
        orders = orders.filter(datetime__gte=minimum_date)

    if maximum_date is not None:
        orders = orders.filter(datetime__lte=maximum_date)

    if minimum_quantity is not None:
        orders = orders.filter(quantity__gte=minimum_quantity)
    
    if maximum_quantity is not None:
        orders = orders.filter(quantity__lte=maximum_quantity)

    if minimum_value is not None:
        orders = orders.filter(total_value__gte=minimum_value)
    
    if maximum_value is not None:
        orders = orders.filter(total_value__lte=maximum_value)

    category = data.get("category")
    if category is not None:
        orders = orders.filter(category=category)

    status = data.get("status")
    if status is not None:
        orders = orders.filter(status=status)

    notes = data.get("notes")
    if notes is not None:
        orders = orders.filter(notes__icontains=notes)

    products = data.get("products")
    if products is not None:
        for related_product in products:
            product_list = related_product.get("product", [])
            if isinstance(product_list, list):
                for product_item in product_list:
                    p_id = product_item.pk if hasattr(product_item, "pk") else product_item
                    orders = orders.filter(products__pk=p_id)
            else:
                p_id = product_list.pk if hasattr(product_list, "pk") else product_list
                orders = orders.filter(products__pk=p_id)

    coupoms = data.get("coupoms")
    if coupoms is not None:
        for related_coupom in coupoms:
            c_id = related_coupom.pk if hasattr(related_coupom, "pk") else related_coupom
            orders = orders.filter(coupoms__pk=c_id)

    return orders


def employee_list_orders(current_employee: Employee, params: dict[str, Any] | Any):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    data = params.validated_data if hasattr(params, "validated_data") else params

    minimum_date = data.get("minimum_date")
    maximum_date = data.get("maximum_date")
    minimum_quantity = data.get("minimum_quantity")
    maximum_quantity = data.get("maximum_quantity")
    minimum_value = data.get("minimum_value")
    maximum_value = data.get("maximum_value")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidOrderDateError

    if (minimum_quantity is not None) and (maximum_quantity is not None):
        if minimum_quantity > maximum_quantity:
            raise InvalidQuantitiesError

    if (minimum_value is not None) and (maximum_value is not None):
        if minimum_value > maximum_value:
            raise InvalidValueError

    orders = Order.objects.all()

    client_id = data.get("client_id")
    if client_id is not None:
        orders = orders.filter(client__id=client_id)

    employee_id = data.get("employee_id")
    if employee_id is not None:
        orders = orders.filter(employee__id=employee_id)

    if minimum_date is not None:
        orders = orders.filter(datetime__gte=minimum_date)

    if maximum_date is not None:
        orders = orders.filter(datetime__lte=maximum_date)

    if minimum_quantity is not None:
        orders = orders.filter(quantity__gte=minimum_quantity)
    
    if maximum_quantity is not None:
        orders = orders.filter(quantity__lte=maximum_quantity)

    if minimum_value is not None:
        orders = orders.filter(total_value__gte=minimum_value)
    
    if maximum_value is not None:
        orders = orders.filter(total_value__lte=maximum_value)

    category = data.get("category")
    if category is not None:
        orders = orders.filter(category=category)

    status = data.get("status")
    if status is not None:
        orders = orders.filter(status=status)

    notes = data.get("notes")
    if notes is not None:
        orders = orders.filter(notes__icontains=notes)

    return orders


def update_order_status(current_employee: Employee, params: dict[str, Any]) -> Order:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_order = Order.objects.get(pk=params["id"])
    except Order.DoesNotExist:
        raise OrderNotFoundError

    target_order.status = params["status"]
    target_order.save()

    return target_order
