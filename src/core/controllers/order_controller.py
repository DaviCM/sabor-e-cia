from core.models import Order, Product, Coupom, ProductsOrders
from core.serializers import CreateOrderSerializer, QueryOrderSerializer, UpdateOrderStatusSerializer
from core.errors import OrderNotFoundError, InvalidValueError, InvalidTotalValueError, InvalidQuantitiesError
from users.models import Client, Employee
from users.errors import ClientNotFoundError, EmployeeNotFoundError, UserHasNoPermissionError

def create_order(current_client: Client, current_employee: Employee, params: CreateOrderSerializer) -> Order:
    if current_client == None:
        raise ClientNotFoundError

    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError

    if params.quantity < 1:
        raise InvalidQuantitiesError

    if params.total_value < 0:
        raise InvalidTotalValueError

    if (params.cover != None) and (params.cover < 0):
        raise InvalidValueError

    new_order = Order(
        quantity=params.quantity,
        total_value=params.total_value,
        category=params.category,
        status=params.status,
        cover=params.cover,
        notes=params.notes,

        client=current_client,
        employee=current_employee,
    )

    for product_entry in params.products:
        new_entry = ProductsOrders(
            product_type=product_entry.product_type,
            is_combo=product_entry.is_combo,

            product=product_entry.product,
            order=new_order,
        )

        new_entry.save()

    if (params.coupoms != None):
        for coupom in params.coupoms:
            new_order.coupoms.add(coupom)

    new_order.save()

    return new_order


def client_list_orders(current_client: Client, params: QueryOrderSerializer):
    if current_client == None:
        raise ClientNotFoundError

# ! TODO: IMPLEMENTAR AMBAS AS FUNÇÕES DE LISTA!!!


def employee_list_orders(current_employee: Employee, params: QueryOrderSerializer):
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError


def update_order_status(current_employee: Employee, params: UpdateOrderStatusSerializer) -> Order:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_order = Order.objects.get(pk=params.id)
    except Order.DoesNotExist:
        raise OrderNotFoundError

    target_order.status = params.status

    target_order.save()

    return target_order
